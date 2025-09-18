"""
基础视图类，用于减少重复代码
"""
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.authentication.permissions import IsActiveUser


class BaseListCreateView(generics.ListCreateAPIView):
    """
    基础列表和创建视图
    """
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        根据请求方法返回不同的序列化器
        """
        if self.request.method == 'POST':
            return self.create_serializer_class
        return self.list_serializer_class


class BaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    基础详情视图
    """
    permission_classes = [IsActiveUser]


class BaseSearchView(generics.ListAPIView):
    """
    基础搜索视图
    """
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']
