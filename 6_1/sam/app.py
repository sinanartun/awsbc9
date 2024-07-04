import json
import whisper
import torch
import boto3
import os
from urllib.parse import unquote_plus

# Initialize the S3 client
s3 = boto3.client('s3', region_name='eu-north-1')

# Ensure torch uses the CPU
device = "cpu"
torch.backends.cudnn.enabled = False
os.environ["TORCH_DEVICE"] = "cpu"
os.environ["FORCE_CPU"] = "1"
os.environ["USE_CUDA"] = "0"

# Load the Whisper model
model = whisper.load_model("small", device=device)

def format_timestamp(seconds):
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def handler(event, context):
    # Extract bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    download_path = f'/tmp/{os.path.basename(key)}'
    upload_path = f'/tmp/{os.path.splitext(os.path.basename(key))[0]}.srt'

    # Download the audio file from S3
    s3.download_file(bucket, key, download_path)

    # Transcribe the entire audio file with fp16 enabled and specified language
    input_language = "en"  # English language code
    result = model.transcribe(download_path, fp16=False, language=input_language)

    # Create the SRT file content
    srt_content = []
    for i, segment in enumerate(result["segments"]):
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        text = segment["text"].strip()
        srt_content.append(f"{i + 1}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(text)
        srt_content.append("")

    # Write the SRT file to the local filesystem
    with open(upload_path, "w") as f:
        f.write("\n".join(srt_content))

    # Upload the SRT file to S3
    s3.upload_file(upload_path, bucket, f"{os.path.splitext(key)[0]}.srt")

    return {
        'statusCode': 200,
        'body': json.dumps('Subtitle file created and uploaded successfully!')
    }

# For local testing
if __name__ == "__main__":
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "awsbc9"
                    },
                    "object": {
                        "key": "story.mp4"
                    }
                }
            }
        ]
    }
    context = {}
    result = handler(event, context)
    print(result)
