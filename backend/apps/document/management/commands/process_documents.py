"""
处理文档管理命令
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.document.models import Document
from services.document_handler import document_handler
from tasks.document_scan import scan_and_process_documents, process_document


class Command(BaseCommand):
    """
    文档处理管理命令
    """
    help = '处理CDR文档文件'
    
    def add_arguments(self, parser):
        """添加命令参数"""
        parser.add_argument(
            '--scan',
            action='store_true',
            help='扫描新文件并加入处理队列',
        )
        parser.add_argument(
            '--process',
            type=int,
            metavar='DOCUMENT_ID',
            help='处理指定的文档ID',
        )
        parser.add_argument(
            '--retry-failed',
            action='store_true',
            help='重试所有失败的文档',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='列出所有文档状态',
        )
        parser.add_argument(
            '--async',
            action='store_true',
            help='异步执行任务（使用Celery）',
        )
    
    def handle(self, *args, **options):
        """处理命令"""
        try:
            if options['scan']:
                self.handle_scan(options['async'])
            elif options['process']:
                self.handle_process(options['process'], options['async'])
            elif options['retry_failed']:
                self.handle_retry_failed(options['async'])
            elif options['list']:
                self.handle_list()
            else:
                self.stdout.write(
                    self.style.ERROR('请指定操作：--scan, --process, --retry-failed, 或 --list')
                )
                
        except Exception as e:
            raise CommandError(f'命令执行失败: {str(e)}')
    
    def handle_scan(self, async_mode=False):
        """处理扫描操作"""
        self.stdout.write('开始扫描新文件...')
        
        if async_mode:
            # 异步执行
            result = scan_and_process_documents.delay()
            self.stdout.write(
                self.style.SUCCESS(f'扫描任务已提交到队列，任务ID: {result.id}')
            )
        else:
            # 同步执行
            new_files = document_handler.scan_for_new_files()
            
            if not new_files:
                self.stdout.write(self.style.WARNING('未发现新文件'))
                return
            
            processed_count = 0
            
            for file_path in new_files:
                try:
                    # 移动文件到processing目录
                    if document_handler.move_file_to_processing(file_path):
                        # 更新文件路径为processing目录
                        processing_file_path = document_handler.processing_dir / file_path.name
                        # 创建文档记录
                        document = document_handler.create_document_record(processing_file_path)
                        
                        if async_mode:
                            # 异步处理文档
                            process_document.delay(document.id)
                        else:
                            # 同步处理文档
                            success = document_handler.process_document(document.id)
                            if success:
                                self.stdout.write(
                                    self.style.SUCCESS(f'文档处理成功: {file_path.name}')
                                )
                            else:
                                self.stdout.write(
                                    self.style.ERROR(f'文档处理失败: {file_path.name}')
                                )
                        
                        processed_count += 1
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'移动文件失败: {file_path.name}')
                        )
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'处理文件 {file_path.name} 时发生异常: {str(e)}')
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(f'扫描完成，共处理 {processed_count} 个文件')
            )
    
    def handle_process(self, document_id, async_mode=False):
        """处理指定文档"""
        try:
            document = Document.objects.get(id=document_id)
            self.stdout.write(f'开始处理文档: {document.filename}')
            
            if async_mode:
                # 异步执行
                result = process_document.delay(document_id)
                self.stdout.write(
                    self.style.SUCCESS(f'处理任务已提交到队列，任务ID: {result.id}')
                )
            else:
                # 同步执行
                success = document_handler.process_document(document_id)
                if success:
                    self.stdout.write(
                        self.style.SUCCESS(f'文档处理成功: {document.filename}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'文档处理失败: {document.filename}')
                    )
                    
        except Document.DoesNotExist:
            raise CommandError(f'文档不存在: {document_id}')
    
    def handle_retry_failed(self, async_mode=False):
        """重试失败的文档"""
        failed_documents = Document.objects.filter(status='failed')
        
        if not failed_documents.exists():
            self.stdout.write(self.style.WARNING('没有失败的文档需要重试'))
            return
        
        self.stdout.write(f'发现 {failed_documents.count()} 个失败的文档')
        
        for document in failed_documents:
            try:
                self.stdout.write(f'重试文档: {document.filename}')
                
                if async_mode:
                    # 异步执行
                    from tasks.document_scan import retry_failed_document
                    result = retry_failed_document.delay(document.id)
                    self.stdout.write(
                        self.style.SUCCESS(f'重试任务已提交到队列，任务ID: {result.id}')
                    )
                else:
                    # 同步执行
                    # 重置文档状态
                    document.status = 'pending'
                    document.error_message = None
                    document.processed_at = None
                    document.processed_iccid_count = 0
                    document.success_iccid_count = 0
                    document.failed_iccid_count = 0
                    document.save()
                    
                    # 重新处理文档
                    success = document_handler.process_document(document.id)
                    if success:
                        self.stdout.write(
                            self.style.SUCCESS(f'文档重试成功: {document.filename}')
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'文档重试失败: {document.filename}')
                        )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'重试文档 {document.filename} 时发生异常: {str(e)}')
                )
                continue
    
    def handle_list(self):
        """列出文档状态"""
        documents = Document.objects.all().order_by('-created_at')
        
        if not documents.exists():
            self.stdout.write(self.style.WARNING('没有文档记录'))
            return
        
        self.stdout.write('\n文档状态列表:')
        self.stdout.write('-' * 100)
        self.stdout.write(
            f'{"ID":<5} {"文件名":<30} {"状态":<10} {"进度":<10} {"成功率":<10} {"创建时间":<20}'
        )
        self.stdout.write('-' * 100)
        
        for doc in documents:
            status_color = {
                'pending': 'yellow',
                'processing': 'blue',
                'success': 'green',
                'failed': 'red'
            }.get(doc.status, 'white')
            
            self.stdout.write(
                f'{doc.id:<5} {doc.filename[:30]:<30} '
                f'{getattr(self.style, status_color.upper())(doc.get_status_display()):<10} '
                f'{doc.progress_percentage:<10.1f}% '
                f'{doc.success_rate:<10.1f}% '
                f'{doc.created_at.strftime("%Y-%m-%d %H:%M:%S"):<20}'
            )
        
        self.stdout.write('-' * 100)
        
        # 统计信息
        total = documents.count()
        pending = documents.filter(status='pending').count()
        processing = documents.filter(status='processing').count()
        success = documents.filter(status='success').count()
        failed = documents.filter(status='failed').count()
        
        self.stdout.write(f'\n统计信息:')
        self.stdout.write(f'总计: {total}')
        self.stdout.write(f'待处理: {pending}')
        self.stdout.write(f'处理中: {processing}')
        self.stdout.write(f'成功: {success}')
        self.stdout.write(f'失败: {failed}')
