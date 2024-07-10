import os
import subprocess
import boto3

# Initialize S3 client
s3 = boto3.client('s3')

# Ensure the /tmp/cache directory exists
cache_dir = '/tmp/cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Function to combine video with subtitles and audio
def combine_video_subtitles_audio(video_path, subtitles_path, audio_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-vf', f"subtitles={subtitles_path}",
        '-c:a', 'aac',
        '-map', '0:v',
        '-map', '1:a',
        '-shortest',
        output_path
    ]
    subprocess.run(command, check=True)
    print('Video, subtitles, and audio combined successfully!')

# Lambda handler function
def lambda_handler(event, context):
    bucket_name = event['bucket_name']
    video_id = event['video_id']
    input_video_path = f'/tmp/{video_id}.mp4'
    translated_srt_path = f'/tmp/{video_id}_tr.srt'
    translated_audio_path = f'/tmp/{video_id}_tr.mp3'
    output_video_path = f'/tmp/{video_id}_translated.mp4'
    video_key = f'{video_id}.mp4'
    translated_srt_key = f'{video_id}_tr.srt'
    translated_audio_key = f'{video_id}_tr.mp3'

    # Download the video, SRT file, and translated audio file from S3
    s3.download_file(bucket_name, video_key, input_video_path)
    s3.download_file(bucket_name, translated_srt_key, translated_srt_path)
    s3.download_file(bucket_name, translated_audio_key, translated_audio_path)

    # Combine video with translated subtitles and audio
    print("Combining video with translated subtitles and audio...")
    combine_video_subtitles_audio(input_video_path, translated_srt_path, translated_audio_path, output_video_path)
    print(f"Combined video saved to {output_video_path}")

    # Upload the combined video back to S3
    combined_video_key = f'{video_id}_translated.mp4'
    s3.upload_file(output_video_path, bucket_name, combined_video_key)

    return {
        'statusCode': 200,
        'video_key': combined_video_key,
        'video_id': video_id
    }
