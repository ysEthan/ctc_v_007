"""
文档扫描和处理任务
"""
import logging
from celery import shared_task
from django.utils import timezone

from apps.document.models import Document
from services.document_handler import document_handler

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def scan_and_process_documents(self):
    """
    扫描并处理新文档
    每6小时执行一次
    """
    try:
        logger.info("开始扫描新文档...")
        
        # 扫描新文件
        new_files = document_handler.scan_for_new_files()
        
        if not new_files:
            logger.info("未发现新文件")
            return "未发现新文件"
        
        processed_count = 0
        
        for file_path in new_files:
            try:
                # 移动文件到processing目录
                if document_handler.move_file_to_processing(file_path):
                    # 更新文件路径为processing目录
                    processing_file_path = document_handler.processing_dir / file_path.name
                    # 创建文档记录
                    document = document_handler.create_document_record(processing_file_path)
                    
                    # 异步处理文档
                    process_document.delay(document.id)
                    
                    processed_count += 1
                    logger.info(f"文档已加入处理队列: {file_path.name}")
                else:
                    logger.error(f"移动文件失败: {file_path.name}")
                    
            except Exception as e:
                logger.error(f"处理文件 {file_path.name} 时发生异常: {str(e)}")
                continue
        
        result = f"扫描完成，共处理 {processed_count} 个文件"
        logger.info(result)
        return result
        
    except Exception as e:
        logger.error(f"扫描文档任务失败: {str(e)}")
        # 重试任务
        raise self.retry(countdown=300, exc=e)  # 5分钟后重试


@shared_task(bind=True, max_retries=2)
def process_document(self, document_id: int):
    """
    处理单个文档
    
    Args:
        document_id: 文档ID
    """
    try:
        logger.info(f"开始处理文档: {document_id}")
        
        # 获取文档记录
        document = Document.objects.get(id=document_id)
        
        # 标记为处理中
        document.mark_as_processing()
        
        # 处理文档
        success = document_handler.process_document(document_id)
        
        if success:
            logger.info(f"文档处理成功: {document.filename}")
            return f"文档处理成功: {document.filename}"
        else:
            logger.error(f"文档处理失败: {document.filename}")
            return f"文档处理失败: {document.filename}"
            
    except Document.DoesNotExist:
        logger.error(f"文档记录不存在: {document_id}")
        return f"文档记录不存在: {document_id}"
    except Exception as e:
        logger.error(f"处理文档任务失败: {str(e)}")
        # 重试任务
        raise self.retry(countdown=60, exc=e)  # 1分钟后重试


@shared_task(bind=True, max_retries=2)
def retry_failed_document(self, document_id: int):
    """
    重试失败的文档
    
    Args:
        document_id: 文档ID
    """
    try:
        logger.info(f"重试处理文档: {document_id}")
        
        # 获取文档记录
        document = Document.objects.get(id=document_id)
        
        if document.status != 'failed':
            logger.warning(f"文档状态不是失败状态: {document.status}")
            return f"文档状态不是失败状态: {document.status}"
        
        # 重置文档状态
        document.status = 'pending'
        document.error_message = None
        document.processed_at = None
        document.processed_iccid_count = 0
        document.success_iccid_count = 0
        document.failed_iccid_count = 0
        document.save()
        
        # 重新处理文档
        process_document.delay(document_id)
        
        logger.info(f"文档已加入重试队列: {document.filename}")
        return f"文档已加入重试队列: {document.filename}"
        
    except Document.DoesNotExist:
        logger.error(f"文档记录不存在: {document_id}")
        return f"文档记录不存在: {document_id}"
    except Exception as e:
        logger.error(f"重试文档任务失败: {str(e)}")
        raise self.retry(countdown=60, exc=e)


@shared_task(bind=True, max_retries=2)
def retry_badcase(self, badcase_id: int):
    """
    重试错误案例
    
    Args:
        badcase_id: 错误案例ID
    """
    try:
        from apps.document.models import BadCase
        from services.data_service import data_service
        
        logger.info(f"重试错误案例: {badcase_id}")
        
        # 获取错误案例记录
        badcase = BadCase.objects.get(id=badcase_id)
        
        if not badcase.can_retry:
            logger.warning(f"错误案例已达到最大重试次数: {badcase_id}")
            return f"错误案例已达到最大重试次数: {badcase_id}"
        
        # 增加重试次数
        badcase.increment_retry()
        
        # 重新处理该ICCID
        success, error_msg = data_service.process_iccid_data(
            badcase.document.id, 
            badcase.iccid
        )
        
        if success:
            logger.info(f"错误案例重试成功: {badcase.iccid}")
            return f"错误案例重试成功: {badcase.iccid}"
        else:
            logger.warning(f"错误案例重试失败: {badcase.iccid} - {error_msg}")
            return f"错误案例重试失败: {badcase.iccid} - {error_msg}"
            
    except BadCase.DoesNotExist:
        logger.error(f"错误案例记录不存在: {badcase_id}")
        return f"错误案例记录不存在: {badcase_id}"
    except Exception as e:
        logger.error(f"重试错误案例任务失败: {str(e)}")
        raise self.retry(countdown=60, exc=e)


@shared_task
def cleanup_old_documents():
    """
    清理旧的文档记录
    定期清理成功处理超过30天的文档记录
    """
    try:
        from datetime import timedelta
        
        # 计算30天前的时间
        cutoff_date = timezone.now() - timedelta(days=30)
        
        # 查找需要清理的文档
        old_documents = Document.objects.filter(
            status='success',
            processed_at__lt=cutoff_date
        )
        
        count = old_documents.count()
        
        if count > 0:
            # 删除旧文档记录
            old_documents.delete()
            logger.info(f"清理了 {count} 个旧文档记录")
            return f"清理了 {count} 个旧文档记录"
        else:
            logger.info("没有需要清理的旧文档记录")
            return "没有需要清理的旧文档记录"
            
    except Exception as e:
        logger.error(f"清理旧文档任务失败: {str(e)}")
        return f"清理旧文档任务失败: {str(e)}"
