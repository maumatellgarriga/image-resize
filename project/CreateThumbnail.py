import boto3
from PIL import Image
import urllib.parse

s3_client = boto3.client('s3')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)
     
def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        download_path = '/tmp/{}'.format(key)
        upload_path = '/tmp/resized-{}'.format(key)
        print(bucket)
        print(key)
        print(download_path)
        print(upload_path)
        #s3_client.download_file(bucket, key, download_path)
        #resize_image(download_path, upload_path)
        #s3_client.upload_file(upload_path, '{}-resized'.format(bucket), key)
