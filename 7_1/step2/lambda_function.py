import json
import os
import subprocess
import boto3

s3 = boto3.client('s3')


def download_from_s3(bucket, key, download_path):
    s3.download_file(bucket, key, download_path)
    print('Download from S3 completed!')

def convert_to_audio(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:a', 'aac',
        output_path
    ]
    subprocess.run(command, check=True)
    print('Conversion to MP3 completed!')

def upload_to_s3(file_path, bucket, key):
    with open(file_path, 'rb') as f:
        s3.upload_fileobj(f, bucket, key)
    print('Upload to S3 completed!')


def lambda_handler(event, context):
    bucket_name = event.get('bucket_name')
    mp4_key = event.get('video_key')
    video_id = os.path.splitext(os.path.basename(mp4_key))[0]
    mp4_path = f'/tmp/{mp4_key}'
    audio_path = f'/tmp/{video_id}.aac'
    

    try:
        download_from_s3(bucket_name, mp4_key, mp4_path)
        convert_to_audio(mp4_path, audio_path)
        upload_to_s3(audio_path, bucket_name, f'{video_id}.aac')
        return {
            'statusCode': 200,
            'video_id': video_id,
            'body': json.dumps('Download, conversion, and upload completed')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Operation failed: {str(e)}')
        }