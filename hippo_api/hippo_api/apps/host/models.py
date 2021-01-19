from django.db import models

# Create your models here.
class Hosts(models.Model):
    name = models.CharField(max_length=32, verbose_name="主机名")
    ip_addr = models.CharField(max_length=32, verbose_name="ip地址")

    class Meta:
        db_table = 't_hippo_hosts'
        verbose_name= '主机表'
        verbose_name_plural = verbose_name