from rest_framework import serializers

from . import models
from hippo_api.libs.ssh import SSH
from hippo_api.utils.check_ssh import valid_ssh
from hippo_api.utils.handle_key import AppSetting


class HostModelSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.Hosts
        fields = ['id', 'password', 'category','category_name', 'hostname',
                  'ip_addr', 'port', 'username', 'desc']
        extra_kwargs = {
            'category':{'write_only':True},
        }

    def validate(self, attrs):
        ip_addr = attrs.get('ip_addr')
        port = attrs.get('port')
        username = attrs.get('username')
        password = attrs.get('password')
        ret = valid_ssh(host=ip_addr,port=port,username=username,password=password)
        if not ret:
            raise serializers.ValidationError('参数校验失败，请核对输入内容')
        return attrs

    def create(self, validated_data):
        ip_addr = validated_data.get("ip_addr")
        port = validated_data.get("port")
        username = validated_data.get("username")
        password = validated_data.get("password")
        ssh = SSH(host=ip_addr, port=port,username=username,password=str(password))
        try:
            private_key = AppSetting.get(key="private_key")
            public_key = AppSetting.get(key="public_key")
        except KeyError:
            private_key, public_key, = ssh.generate_key()
            AppSetting.set(key="private_key", value=private_key,desc="ssh private key")
            AppSetting.set(key="public_key", value=public_key,desc="ssh public key")
        ssh.add_public_key(public_key=public_key)

        password = validated_data.pop("password")
        new_host_obj = models.Hosts.objects.create(
            **validated_data
        )
        return new_host_obj


class HostCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HostCategory
        fields = ['id', 'name']
