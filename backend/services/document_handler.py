"""
文档处理服务
处理CDR文件的扫描、解析和处理
"""
import os
import re
import shutil
import csv
import logging
from typing import List, Dict, Any, Set
from pathlib import Path
from django.conf import settings
from django.utils import timezone

from apps.document.models import Document
from .data_service import data_service

logger = logging.getLogger(__name__)


class DocumentHandler:
    """
    文档处理器
    负责CDR文件的扫描、解析和处理
    """
    
    def __init__(self):
        # 文件路径配置
        self.cdr_root = Path("/data/cdr")
        self.processing_dir = self.cdr_root / "processing"
        self.success_dir = self.cdr_root / "success"
        self.failed_dir = self.cdr_root / "failed"
        
        # 确保目录存在
        self._ensure_directories()
        
        # 文件名解析正则表达式
        # 格式: [前缀]_[记录类型]_[主机节点]_[CDR类型]_[版本]_[日期].csv
        self.filename_pattern = re.compile(
            r'^(.+)_([^_]+)_([^_]+)_([^_]+)_([^_]+)_(\d{8})\.csv$'
        )
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        for directory in [self.processing_dir, self.success_dir, self.failed_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def scan_for_new_files(self) -> List[Path]:
        """
        扫描新文件
        
        Returns:
            List[Path]: 新文件路径列表
        """
        new_files = []
        
        try:
            # 扫描CDR根目录
            for file_path in self.cdr_root.iterdir():
                if (file_path.is_file() and 
                    file_path.suffix.lower() == '.csv' and
                    file_path.name not in ['processing', 'success', 'failed']):
                    
                    # 验证文件名格式
                    if self._is_valid_filename(file_path.name):
                        new_files.append(file_path)
                    else:
                        logger.warning(f"文件名格式不正确，跳过: {file_path.name}")
            
            logger.info(f"扫描到 {len(new_files)} 个新文件")
            return new_files
            
        except Exception as e:
            logger.error(f"扫描文件时发生异常: {str(e)}")
            return []
    
    def _is_valid_filename(self, filename: str) -> bool:
        """
        验证文件名格式
        
        Args:
            filename: 文件名
            
        Returns:
            bool: 是否有效
        """
        match = self.filename_pattern.match(filename)
        return match is not None
    
    def parse_filename(self, filename: str) -> Dict[str, str]:
        """
        解析文件名
        
        Args:
            filename: 文件名
            
        Returns:
            Dict[str, str]: 解析结果
        """
        match = self.filename_pattern.match(filename)
        if not match:
            return {}
        
        return {
            'file_prefix': match.group(1),
            'record_type': match.group(2),
            'host_node': match.group(3),
            'cdr_type': match.group(4),
            'version': match.group(5),
            'file_date': match.group(6)
        }
    
    def move_file_to_processing(self, file_path: Path) -> bool:
        """
        将文件移动到processing目录
        
        Args:
            file_path: 源文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            dest_path = self.processing_dir / file_path.name
            shutil.move(str(file_path), str(dest_path))
            logger.info(f"文件已移动到processing目录: {file_path.name}")
            return True
        except Exception as e:
            logger.error(f"移动文件到processing目录失败: {str(e)}")
            return False
    
    def move_file_to_success(self, file_path: Path) -> bool:
        """
        将文件移动到success目录
        
        Args:
            file_path: 源文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            dest_path = self.success_dir / file_path.name
            shutil.move(str(file_path), str(dest_path))
            logger.info(f"文件已移动到success目录: {file_path.name}")
            return True
        except Exception as e:
            logger.error(f"移动文件到success目录失败: {str(e)}")
            return False
    
    def move_file_to_failed(self, file_path: Path) -> bool:
        """
        将文件移动到failed目录
        
        Args:
            file_path: 源文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            dest_path = self.failed_dir / file_path.name
            shutil.move(str(file_path), str(dest_path))
            logger.info(f"文件已移动到failed目录: {file_path.name}")
            return True
        except Exception as e:
            logger.error(f"移动文件到failed目录失败: {str(e)}")
            return False
    
    def create_document_record(self, file_path: Path) -> Document:
        """
        创建文档记录
        
        Args:
            file_path: 文件路径
            
        Returns:
            Document: 文档实例
        """
        # 解析文件名
        filename_info = self.parse_filename(file_path.name)
        
        # 获取文件大小
        file_size = file_path.stat().st_size
        
        # 创建文档记录
        document = Document.objects.create(
            filename=file_path.name,
            file_path=str(file_path),
            file_size=file_size,
            file_prefix=filename_info.get('file_prefix'),
            record_type=filename_info.get('record_type'),
            host_node=filename_info.get('host_node'),
            cdr_type=filename_info.get('cdr_type'),
            version=filename_info.get('version'),
            file_date=filename_info.get('file_date'),
            status='processing'
        )
        
        logger.info(f"创建文档记录: {document.id} - {file_path.name}")
        return document
    
    def parse_csv_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        解析CSV文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            List[Dict[str, Any]]: 解析后的数据列表
        """
        data_list = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                # 使用分号作为分隔符
                reader = csv.reader(csvfile, delimiter=',')
                
                for row_num, row in enumerate(reader, 1):
                    if not row or len(row) < 7:  # 至少需要7个字段
                        continue
                    
                    # 解析CSV行数据
                    # 格式: DATE,IMSI,MSISDN,ICCID,MCC,MNC,USAGE,USAGE_CHARGED
                    try:
                        data = {
                            'date': row[0].strip(),
                            'imsi': row[1].strip(),
                            'msisdn': row[2].strip(),
                            'iccid': row[3].strip(),
                            'mcc': row[4].strip(),
                            'mnc': row[5].strip(),
                            'usage': int(row[6].strip()) if row[6].strip() else 0,
                            'usage_charged': int(row[7].strip()) if len(row) > 7 and row[7].strip() else 0,
                            'row_number': row_num
                        }
                        
                        # 验证必要字段
                        # ICCID标准长度是19-20位，且应该以89开头
                        if (data['iccid'] and 
                            len(data['iccid']) in [19, 20] and 
                            data['iccid'].startswith('89') and
                            data['iccid'].isdigit()):
                            data_list.append(data)
                        else:
                            logger.warning(f"第{row_num}行ICCID格式不正确: {data['iccid']}")
                            
                    except (ValueError, IndexError) as e:
                        logger.warning(f"第{row_num}行数据解析失败: {str(e)}")
                        continue
            
            logger.info(f"CSV文件解析完成，共{len(data_list)}条有效记录")
            return data_list
            
        except Exception as e:
            logger.error(f"解析CSV文件失败: {str(e)}")
            return []
    
    def extract_unique_iccids(self, data_list: List[Dict[str, Any]]) -> Set[str]:
        """
        提取唯一的ICCID列表
        
        Args:
            data_list: 数据列表
            
        Returns:
            Set[str]: 唯一ICCID集合
        """
        iccids = set()
        for data in data_list:
            if data.get('iccid'):
                iccids.add(data['iccid'])
        
        logger.info(f"提取到 {len(iccids)} 个唯一ICCID")
        return iccids
    
    def process_document(self, document_id: int) -> bool:
        """
        处理文档
        
        Args:
            document_id: 文档ID
            
        Returns:
            bool: 是否处理成功
        """
        try:
            # 获取文档记录
            document = Document.objects.get(id=document_id)
            file_path = Path(document.file_path)
            
            # 检查文件是否存在
            if not file_path.exists():
                logger.error(f"文件不存在: {file_path}")
                document.mark_as_failed("文件不存在")
                return False
            
            # 解析CSV文件
            data_list = self.parse_csv_file(file_path)
            if not data_list:
                logger.error(f"CSV文件解析失败或为空: {file_path}")
                document.mark_as_failed("CSV文件解析失败或为空")
                return False
            
            # 提取唯一ICCID
            unique_iccids = self.extract_unique_iccids(data_list)
            if not unique_iccids:
                logger.error(f"未找到有效的ICCID: {file_path}")
                document.mark_as_failed("未找到有效的ICCID")
                return False
            
            # 更新文档统计信息
            document.total_iccid_count = len(unique_iccids)
            document.save()
            
            # 处理每个ICCID
            success_count = 0
            failed_count = 0
            
            for iccid in unique_iccids:
                try:
                    # 处理ICCID数据
                    success, error_msg = data_service.process_iccid_data(document_id, iccid)
                    
                    if success:
                        success_count += 1
                    else:
                        failed_count += 1
                        logger.warning(f"处理ICCID {iccid} 失败: {error_msg}")
                    
                    # 更新处理进度
                    document.processed_iccid_count += 1
                    document.success_iccid_count = success_count
                    document.failed_iccid_count = failed_count
                    document.save()
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"处理ICCID {iccid} 时发生异常: {str(e)}")
            
            # 判断整体处理结果
            if failed_count == 0:
                # 全部成功
                document.mark_as_success()
                self.move_file_to_success(file_path)
                logger.info(f"文档处理成功: {document.filename}")
                return True
            elif success_count > 0:
                # 部分成功
                document.mark_as_success()  # 部分成功也标记为成功
                self.move_file_to_success(file_path)
                logger.info(f"文档处理完成（部分成功）: {document.filename}")
                return True
            else:
                # 全部失败
                document.mark_as_failed("所有ICCID处理失败")
                self.move_file_to_failed(file_path)
                logger.error(f"文档处理失败: {document.filename}")
                return False
                
        except Document.DoesNotExist:
            logger.error(f"文档记录不存在: {document_id}")
            return False
        except Exception as e:
            logger.error(f"处理文档时发生异常: {str(e)}")
            try:
                document = Document.objects.get(id=document_id)
                document.mark_as_failed(f"处理异常: {str(e)}")
                # 移动文件到失败目录
                file_path = Path(document.file_path)
                if file_path.exists():
                    self.move_file_to_failed(file_path)
            except:
                pass
            return False


# 全局文档处理器实例
document_handler = DocumentHandler()
