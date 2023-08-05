

# https://github.com/Miserlou/Zappa/issues/1123

print("============zappa_commands.py================")
import os
import sys
class Runner:
    def __getattr__(self, attr):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtxcms.settings.base')
        from django.core.management import call_command
        print("xxxxxxxxxxxxxxxxxxxxxxxxx zappa_commands.py xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return lambda: call_command(attr)


sys.modules[__name__] = Runner()