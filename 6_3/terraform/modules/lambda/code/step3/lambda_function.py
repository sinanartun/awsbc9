import json
import re
import os
from datetime import datetime
import boto3
import urllib3
from botocore.exceptions import ClientError

def extract_data(raw_data, symbol):
    regex = re.compile(r'\[\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\s*\]')
    csv_data = 'date,high,low,close,volume\n'
    matches = regex.findall(raw_data)
    for match in matches:
        if match and match[0]:
            unix_time = float(match[0])
            date = unix_time
            data_array = match[1:]
            csv_data += f"{date},{','.join(data_array)}\n"
    if csv_data != 'date,high,low,close,volume\n':
        with open(f'/tmp/{symbol}.csv', 'w') as f:
            f.write(csv_data)
        return csv_data
    else:
        raise ValueError('No data found')

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True

def lambda_handler(event, context):
    # Get environment variables
    bucket_name = os.environ['BUCKET_NAME']
    
    body = json.loads(event['Records'][0]['body'])
    symbol = body[0]
    urlpart = body[1]

    url = f'https://finans.mynet.com/borsa/hisseler/{urlpart}'
    
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    
    if response.status != 200:
        raise ValueError(f"Request to {url} failed with status {response.status}")
    
    raw_data = response.data.decode('utf-8')
    
    csv_res = extract_data(raw_data, symbol)
    
    upload_to_s3(f'/tmp/{symbol}.csv', bucket_name, f'bist/{symbol}.csv')
    
    return {
        'statusCode': 200,
        'body': json.dumps(csv_res)
    }
