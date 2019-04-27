from django.apps import AppConfig
# 经源码分析，admin就是这样先导入这个
from django.utils.module_loading import autodiscover_modules


class StarkConfig(AppConfig):
    name = 'stark'

    def ready(self):
        autodiscover_modules("stark")