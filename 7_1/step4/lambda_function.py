import os
import srt
import boto3
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
from pydub import AudioSegment

s3 = boto3.client('s3')
if not os.path.exists('/tmp/cache'):
    os.makedirs('/tmp/cache')

# Function to read and parse the SRT file
def read_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    subtitles = list(srt.parse(content))
    return subtitles

# Function to translate text to the target language
def translate_text(text, model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name, save_directory='/tmp/cache', cache_dir='/tmp/cache')
    model = MarianMTModel.from_pretrained(model_name, save_directory='/tmp/cache')
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    translated_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return translated_text[0]

# Function to translate subtitles
def translate_subtitles(subtitles, model_name):
    translated_subtitles = []
    for subtitle in subtitles:
        translated_content = translate_text(subtitle.content, model_name)
        subtitle.content = translated_content
        translated_subtitles.append(subtitle)
    return translated_subtitles

# Function to write the translated subtitles to a new SRT file
def write_srt_file(subtitles, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(srt.compose(subtitles))

# Function to convert text to speech and save as audio file
def srt_to_audio(subtitles, lang, output_path, video_id):
    combined_audio = AudioSegment.empty()
    for subtitle in subtitles:
        tts = gTTS(subtitle.content, lang=lang)
        temp_audio_path = f'/tmp/{video_id}_temp.aac'
        tts.save(temp_audio_path)
        audio_segment = AudioSegment.from_aac(temp_audio_path)
        combined_audio += audio_segment
    combined_audio.export(output_path, format='aac')


def lambda_handler(event, context):
    bucket_name = event['bucket_name']
    video_id = event['video_id']
    model_name = 'Helsinki-NLP/opus-tatoeba-en-tr'  # Correct model for English to Turkish translation
    input_srt_path = f'/tmp/{video_id}.srt'
    tgt_lang = 'tr'
    translated_srt_path = f'/tmp/{video_id}_tr.srt'
    output_audio_path = f'/tmp/{video_id}.aac'
    srt_key = f'{video_id}.srt'

    # Download the SRT file from S3
    s3.download_file(bucket_name, srt_key, input_srt_path)

    # Step 1: Read and translate the SRT file
    print("Reading and translating SRT file...")
    subtitles = read_srt_file(input_srt_path)
    translated_subtitles = translate_subtitles(subtitles, model_name)
    write_srt_file(translated_subtitles, translated_srt_path)
    print(f"Translated SRT file saved to {translated_srt_path}")

    # Step 2: Convert the translated subtitles to an audio file
    print("Converting translated subtitles to audio...")
    srt_to_audio(translated_subtitles, tgt_lang, output_audio_path, video_id)
    print(f"Audio file saved to {output_audio_path}")

    # Upload the translated SRT file and the audio file back to S3
    translated_srt_key = srt_key.replace('.srt', f'_{tgt_lang}.srt')
    output_audio_key = srt_key.replace('.srt', f'_{tgt_lang}.aac')

    s3.upload_file(translated_srt_path, bucket_name, translated_srt_key)
    s3.upload_file(output_audio_path, bucket_name, output_audio_key)

    return {
        'statusCode': 200,
        'srt_key': translated_srt_key,
        'audio_key': output_audio_key,
        'video_id': video_id
    }
