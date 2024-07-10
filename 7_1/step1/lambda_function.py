#python3.9
import json
import os
import boto3
from yt_dlp import YoutubeDL

s3 = boto3.client('s3')

def lambda_handler(event, context):
    video_url = 'https://www.youtube.com/watch?v=l0Z8A4u3CtI'
    bucket_name = os.environ['BUCKET_NAME']
    
    try:
        save_path, file_name = download_video(video_url)
        upload_to_s3(save_path, bucket_name, file_name)
        return {
            'statusCode': 200,
            'body': json.dumps('Download and upload completed')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Operation failed: {str(e)}')
        }

def download_video(url):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': '/tmp/%(id)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
    print('Download completed!')
    return file_name, os.path.basename(file_name)

def upload_to_s3(file_path, bucket, key):
    with open(file_path, 'rb') as f:
        s3.upload_fileobj(f, bucket, key)
    print('Upload to S3 completed!')
