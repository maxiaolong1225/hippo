from django.shortcuts import render
from rest_framework.generics import ListAPIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from . import models
from .serializers import HostModelSerializer,HostCategoryModelSerializer


class HostView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = models.Hosts.objects.filter(is_show=True, is_deleted=False)
    # queryset = models.Hosts.objects.all()
    serializer_class = HostModelSerializer


class HostCategoryView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = models.HostCategory.objects.filter(is_show=True, is_deleted=False)
    # queryset = models.HostCategory.objects.all()
    serializer_class = HostCategoryModelSerializer