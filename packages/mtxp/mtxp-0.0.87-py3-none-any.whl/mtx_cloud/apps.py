from django.apps import apps
from django.apps import AppConfig
class MtxCloudConfig(AppConfig):
    name='mtx_cloud'
    def ready(self):
        # importing model classes
        # 此时可以访问models
        from .models import SshHost  # or...
        # MyModel = self.get_model('MyModel')

        # registering signals with the model's string label
        # pre_save.connect(receiver, sender='app_label.MyModel')
        
        # print(' config ..........init')
        # print(apps)
        pass