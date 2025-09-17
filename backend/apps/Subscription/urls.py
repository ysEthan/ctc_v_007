"""
订阅URL配置
"""
from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    # 订阅基础CRUD
    path('', views.SubscriptionListView.as_view(), name='subscription-list'),
    path('<int:pk>/', views.SubscriptionDetailView.as_view(), name='subscription-detail'),
    
    # 订阅搜索
    path('search/', views.SubscriptionSearchView.as_view(), name='subscription-search'),
    
    # 订阅统计
    path('statistics/', views.subscription_statistics, name='subscription-statistics'),
    
    # 订阅批量操作
    path('bulk-import/', views.subscription_bulk_import, name='subscription-bulk-import'),
    path('export/', views.subscription_export, name='subscription-export'),
]
