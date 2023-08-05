import boto3
from pathlib import Path
s3_client = boto3.client('s3')

from zappa.asynchronous import task

def handler(event, context):
    print(f"s3_event_handler: event: {event} context: {context}") 
 
    # Get the uploaded file's information
    bucket = event['Records'][0]['s3']['bucket']['name'] # Will be `my-bucket`
    key = event['Records'][0]['s3']['object']['key'] # Will be the file path of whatever file was uploaded.

    print(f"bucket:{bucket},key: {key}")
    # Get the bytes from S3
    
    s3_client.download_file(bucket, key, '/tmp/' + key) # Download this file to writable tmp space.
    file_bytes = open('/tmp/' + key).read()
    print("读取的文件长度"+ str(len(file_bytes)))