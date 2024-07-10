import boto3
import whisper
import torch
import os

# Initialize the S3 client
s3 = boto3.client('s3')

# Check if a CUDA-enabled GPU is available
device = "cpu"

# Use /tmp directory for model download
download_root = "/tmp/whisper_model"

def download_file_from_s3(bucket_name, key, download_path):
    s3.download_file(bucket_name, key, download_path)

def upload_file_to_s3(file_path, bucket_name, key):
    s3.upload_file(file_path, bucket_name, key)

def format_timestamp(seconds):
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def create_srt_content(result):
    srt_content = []
    for i, segment in enumerate(result["segments"]):
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        text = segment["text"].strip()
        srt_content.append(f"{i + 1}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(text)
        srt_content.append("")
    return "\n".join(srt_content)

def lambda_handler(event, context):
    # Extract bucket name and file key from the event
    bucket_name = event['bucket_name']
    audio_key = event['audio_key']
    video_id = os.path.splitext(os.path.basename(audio_key))[0]
    # Define local paths
    local_audio_path = f"/tmp/{video_id}.mp3"
    local_srt_path = f"/tmp/{video_id}.srt"
    
    # Download the video file from S3
    download_file_from_s3(bucket_name, audio_key, local_audio_path)
    
    # Load the Whisper model
    model = whisper.load_model("small.en", device=device, download_root=download_root)
    
    # Transcribe the audio
    input_language = "en"  # English language code
    result = model.transcribe(local_audio_path, fp16=False, language=input_language)
    
    # Create SRT content
    srt_content = create_srt_content(result)
    
    # Write the SRT file locally
    with open(local_srt_path, "w") as f:
        f.write(srt_content)
    
    # Upload the SRT file to S3
    output_key = video_id + ".srt"
    upload_file_to_s3(local_srt_path, bucket_name, output_key)
    
    return {
        'statusCode': 200,
        'video_id': video_id
    }