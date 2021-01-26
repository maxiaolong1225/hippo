from functools import lru_cache

from host.models import PkeyModel


class AppSetting:
    keys = ('public_key','private_key')

    @classmethod
    @lru_cache(maxsize=64)
    def get(cls, key):
        info = PkeyModel.objects.filter(key=key).first()
        if not info:
            raise KeyError("密钥%s不存在" % key)
        return info.value

    @classmethod
    def set(cls, key, value, desc=None):
        if key in cls.keys:
            PkeyModel.objects.update_or_create(key=key,defaults={'value':value, 'desc':desc})
        else:
            raise KeyError("key数据不正常")
