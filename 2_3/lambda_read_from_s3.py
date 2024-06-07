import boto3
import os

def lambda_handler(event, context):
    # Define S3 client
    s3 = boto3.client('s3')
    
    # The bucket name and file key are expected to be passed in the event
    bucket_name = "awsbc9"
    file_key = "data.txt"
    
    try:
        # Get the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        
        # Read the content of the file
        file_content = response['Body'].read().decode('utf-8')
        
        return {
            'statusCode': 200,
            'body': file_content
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
