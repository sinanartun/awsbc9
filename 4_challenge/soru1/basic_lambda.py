import boto3
import datetime

def lambda_handler(event, context):
    
    s3 = boto3.client('s3', region_name='us-east-2')

    current_time = datetime.datetime.now()
    bucket_name = 'challenge-' + current_time.strftime('%Y-%m-%d-%H-%M-%S')

    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-east-2'}
        )

        return {
            'statusCode': 200,
            'body': f'S3 bucket "{bucket_name}" created successfully!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error creating bucket: {str(e)}'
        }
