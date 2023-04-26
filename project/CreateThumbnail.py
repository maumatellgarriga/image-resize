import boto3
from PIL import Image
import urllib.parse
import os

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        print("start resize...")
        image.thumbnail((350, 350))
        print("...resized")
        if not os.path.exists(os.path.dirname(resized_path)):
            os.makedirs(os.path.dirname(resized_path))
        image.save(resized_path)

def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        download_path = '/tmp/{}'.format(key)
        upload_path = '/tmp/resized-{}'.format(key)
        
        if not os.path.exists(os.path.dirname(download_path)):
            os.makedirs(os.path.dirname(download_path))
        s3_resource.meta.client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        upload_bucket = '{}-resized'.format(bucket)
        upload_key = key
        s3_client.upload_file(upload_path, upload_bucket, upload_key)
