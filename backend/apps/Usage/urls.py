"""
用量URL配置
"""
from django.urls import path
from . import views

app_name = 'usage'

urlpatterns = [
    # 用量基础CRUD
    path('', views.UsageListView.as_view(), name='usage-list'),
    path('<int:pk>/', views.UsageDetailView.as_view(), name='usage-detail'),
    
    # 用量搜索
    path('search/', views.UsageSearchView.as_view(), name='usage-search'),
    
    # 用量统计
    path('statistics/', views.usage_statistics, name='usage-statistics'),
    path('daily-statistics/', views.usage_daily_statistics, name='usage-daily-statistics'),
    
    # 用量批量操作
    path('bulk-import/', views.usage_bulk_import, name='usage-bulk-import'),
    path('export/', views.usage_export, name='usage-export'),
]
