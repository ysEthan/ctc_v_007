"""
ICC URL配置
"""
from django.urls import path
from . import views

app_name = 'icc'

urlpatterns = [
    # ICC基础CRUD
    path('', views.ICCListView.as_view(), name='icc-list'),
    path('<int:pk>/', views.ICCDetailView.as_view(), name='icc-detail'),
    
    # ICC搜索
    path('search/', views.ICCSearchView.as_view(), name='icc-search'),
    
    # ICC统计
    path('statistics/', views.icc_statistics, name='icc-statistics'),
    
    # ICC批量操作
    path('bulk-import/', views.icc_bulk_import, name='icc-bulk-import'),
    path('export/', views.icc_export, name='icc-export'),
]
