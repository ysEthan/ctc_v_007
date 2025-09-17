"""
文档管理URL配置
"""
from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    # 文档基础CRUD
    path('', views.DocumentListView.as_view(), name='document-list'),
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    
    # 文档搜索
    path('search/', views.DocumentSearchView.as_view(), name='document-search'),
    
    # 文档统计
    path('statistics/', views.document_statistics, name='document-statistics'),
    
    # 文档重试
    path('<int:document_id>/retry/', views.retry_failed_document, name='document-retry'),
    
    # 扫描新文档
    path('scan/', views.scan_new_documents, name='document-scan'),
    
    # 错误案例
    path('badcases/', views.BadCaseListView.as_view(), name='badcase-list'),
    path('badcases/<int:pk>/', views.BadCaseDetailView.as_view(), name='badcase-detail'),
    path('badcases/<int:badcase_id>/retry/', views.retry_badcase, name='badcase-retry'),
    
    # 错误案例统计
    path('badcases/statistics/', views.badcase_statistics, name='badcase-statistics'),
]
