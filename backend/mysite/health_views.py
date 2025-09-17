"""
健康检查视图
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core.cache import cache
import redis
import os


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    健康检查端点
    """
    health_status = {
        'status': 'healthy',
        'timestamp': None,
        'services': {}
    }
    
    try:
        from django.utils import timezone
        health_status['timestamp'] = timezone.now().isoformat()
    except Exception:
        import datetime
        health_status['timestamp'] = datetime.datetime.now().isoformat()
    
    # 检查数据库连接
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['services']['database'] = 'healthy'
    except Exception as e:
        health_status['services']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # 检查Redis连接
    try:
        redis_host = os.getenv('REDIS_HOST', 'redis')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        r.ping()
        health_status['services']['redis'] = 'healthy'
    except Exception as e:
        health_status['services']['redis'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # 检查缓存
    try:
        cache.set('health_check', 'ok', 10)
        cache.get('health_check')
        health_status['services']['cache'] = 'healthy'
    except Exception as e:
        health_status['services']['cache'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # 返回状态码
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return JsonResponse(health_status, status=status_code)
