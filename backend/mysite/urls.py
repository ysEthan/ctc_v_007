"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .health_views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    
    # JWT认证端点
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 认证相关API
    path('api/auth/', include('apps.authentication.urls')),
    
    # ICC管理API
    path('api/icc/', include('apps.ICC.urls')),
    
    # 订阅管理API
    path('api/subscription/', include('apps.Subscription.urls')),
    
    # 用量管理API
    path('api/usage/', include('apps.Usage.urls')),
    
    # 文档管理API
    path('api/document/', include('apps.document.urls')),
    
    # DRF API端点
    path('api/', include('rest_framework.urls')),
]
