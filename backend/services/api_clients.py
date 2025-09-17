"""
BSS API客户端
基于提供的API脚本封装
"""
import hashlib
import json
import time
import uuid
import requests
import os
from typing import Dict, Any, Optional
import urllib3
from django.conf import settings

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BSSAPIClient:
    """BSS API客户端"""
    
    def __init__(self):
        """
        初始化API客户端
        从Django设置中获取配置
        """
        self.base_url = getattr(settings, 'BSS_API_BASE_URL', 'https://202.77.19.198')
        self.app_id = getattr(settings, 'BSS_API_APP_ID', 'A10000000013')
        self.app_secret = getattr(settings, 'BSS_API_APP_SECRET', '0D13F9A39A024BBF930945221BDF5668')
        
        # 确保base_url不以斜杠结尾
        self.base_url = self.base_url.rstrip('/')
        
    def _generate_signature(self, trans_id: str, timestamp: str) -> str:
        """
        生成MD5签名
        按照文档要求：Ciphertext=MD5(AppId+TransId+Timestamp+AppSecret)
        """
        sign_string = f"{self.app_id}{trans_id}{timestamp}{self.app_secret}"
        return hashlib.md5(sign_string.encode('utf-8')).hexdigest()
    
    def _get_headers(self, trans_id: str, timestamp: str) -> Dict[str, str]:
        """
        获取请求头
        """
        ciphertext = self._generate_signature(trans_id, timestamp)
        
        return {
            'AppId': self.app_id,
            'TransId': trans_id,
            'Timestamp': timestamp,
            'Ciphertext': ciphertext,
            'Locale': 'cn',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, endpoint: str, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """
        通用请求方法
        """
        # 生成请求参数
        trans_id = str(uuid.uuid4())
        timestamp = str(int(time.time() * 1000))  # 毫秒时间戳
        
        # 请求头
        headers = self._get_headers(trans_id, timestamp)
        
        # API端点
        url = f"{self.base_url}{endpoint}"
        
        try:
            # 发送POST请求
            response = requests.post(
                url=url,
                headers=headers,
                json=request_body,
                timeout=30,
                verify=False  # 如果使用自签名证书，设置为False
            )
            
            # 解析响应
            result = response.json()
            result['_request_info'] = {
                'url': url,
                'headers': headers,
                'request_body': request_body,
                'status_code': response.status_code,
                'trans_id': trans_id
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "请求异常",
                "message": str(e),
                "transId": trans_id,
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
        except json.JSONDecodeError as e:
            return {
                "error": "响应解析异常",
                "message": str(e),
                "transId": trans_id
            }
        except Exception as e:
            return {
                "error": "未知异常",
                "message": str(e),
                "transId": trans_id
            }
    
    def query_user_by_iccid(self, iccid: str) -> Dict[str, Any]:
        """
        根据ICCID查询用户信息
        """
        request_body = {
            "userIdentity": {
                "iccid": iccid
            }
        }
        
        return self._make_request("/bossapi/v3/business/user/query", request_body)
    
    def query_subscriptions_by_iccid(self, iccid: str) -> Dict[str, Any]:
        """
        根据ICCID查询订阅信息
        """
        request_body = {
            "userIdentity": {
                "iccid": iccid
            }
        }
        
        return self._make_request("/bossapi/v3/business/subscription/query", request_body)
    
    def query_daily_usage_by_iccid(self, iccid: str, begin_date: str = None, end_date: str = None, usage_type: str = None) -> Dict[str, Any]:
        """
        根据ICCID查询日用量信息
        """
        request_body = {
            "userIdentity": {
                "iccid": iccid
            }
        }
        
        # 添加可选参数
        if begin_date:
            request_body["beginDate"] = begin_date
        if end_date:
            request_body["endDate"] = end_date
        if usage_type:
            request_body["usageType"] = usage_type
        
        return self._make_request("/bossapi/v3/business/usage/query/daily", request_body)


class APIClientManager:
    """
    API客户端管理器
    提供并发控制和重试机制
    """
    
    def __init__(self, max_concurrent=5, max_retries=2, retry_delay=5):
        """
        初始化管理器
        
        Args:
            max_concurrent: 最大并发数
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
        """
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.client = BSSAPIClient()
    
    def query_user_info(self, iccid: str) -> Dict[str, Any]:
        """
        查询用户信息（带重试机制）
        """
        for attempt in range(self.max_retries + 1):
            result = self.client.query_user_by_iccid(iccid)
            
            # 检查是否成功
            if result.get("code") == "0000":
                return result
            
            # 如果不是最后一次尝试，等待后重试
            if attempt < self.max_retries:
                time.sleep(self.retry_delay)
        
        return result
    
    def query_subscription_info(self, iccid: str) -> Dict[str, Any]:
        """
        查询订阅信息（带重试机制）
        """
        for attempt in range(self.max_retries + 1):
            result = self.client.query_subscriptions_by_iccid(iccid)
            
            # 检查是否成功
            if result.get("code") == "0000":
                return result
            
            # 如果不是最后一次尝试，等待后重试
            if attempt < self.max_retries:
                time.sleep(self.retry_delay)
        
        return result
    
    def query_usage_info(self, iccid: str, begin_date: str = None, end_date: str = None, usage_type: str = None) -> Dict[str, Any]:
        """
        查询用量信息（带重试机制）
        """
        for attempt in range(self.max_retries + 1):
            result = self.client.query_daily_usage_by_iccid(iccid, begin_date, end_date, usage_type)
            
            # 检查是否成功
            if result.get("code") == "0000":
                return result
            
            # 如果不是最后一次尝试，等待后重试
            if attempt < self.max_retries:
                time.sleep(self.retry_delay)
        
        return result


# 全局API客户端管理器实例
api_client_manager = APIClientManager(max_concurrent=5, max_retries=2, retry_delay=5)

