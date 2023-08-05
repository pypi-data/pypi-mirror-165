
import os
import sys
import boto3
from django.core.management import call_command
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtxcms.settings.base')
        
def handler(event, context):
    print(f"s3_event_handler: event: {event} context: {context}") 
    print("定时任务：mtx_collectstatic")    
    call_command("mtx_collectstatic")
    return "djcommand_handler.py finished"
    