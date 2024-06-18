import boto3
import json
import datetime
import time
import os
import zipfile
import tempfile

# Initialize boto3 clients
iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda', region_name='us-east-2')

# Function to create an IAM role
def create_iam_role(role_name):
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        # Create the IAM role
        role = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
            Description="Role to allow Lambda function to access S3"
        )
        print(f"Created role {role_name}")
        
        # Attach the S3 full access policy to the role
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
        )
        print(f"Attached S3 full access policy to role {role_name}")
        
        # Wait for the role to be fully propagated
        time.sleep(10)
        
        return role['Role']['Arn']
    except Exception as e:
        print(f"Error creating IAM role: {str(e)}")
        return None

# Function to create a ZIP file for Lambda function code
def create_lambda_deployment_package(file_name, code):
    with open(file_name, 'w') as f:
        f.write(code)
    
    zip_file_name = os.path.join(tempfile.gettempdir(), 'lambda_function.zip')
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        zipf.write(file_name, os.path.basename(file_name))
    
    return zip_file_name

# Function to create a Lambda function
def create_lambda_function(function_name, role_arn):
    lambda_code = """
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
    """
    
    file_name = os.path.join(tempfile.gettempdir(), 'lambda_function.py')
    zip_file_name = create_lambda_deployment_package(file_name, lambda_code)
    
    try:
        with open(zip_file_name, 'rb') as f:
            zipped_code = f.read()

        # Create the Lambda function
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.12',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Timeout=60,
            MemorySize=256
        )
        print(f"Created Lambda function {function_name}")
        return response['FunctionArn']
    except Exception as e:
        print(f"Error creating Lambda function: {str(e)}")
        return None

# Function to invoke the Lambda function
def invoke_lambda_function(function_name):
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse'
        )
        response_payload = json.loads(response['Payload'].read())
        print(f"Lambda response: {response_payload}")
    except Exception as e:
        print(f"Error invoking Lambda function: {str(e)}")

# Main script execution
if __name__ == "__main__":
    current_time = datetime.datetime.now()
    salt = current_time.strftime('%Y-%m-%d-%H-%M-%S')
    role_name = 'v2Challenge-LambdaS3FullAccessRole-' + salt
    function_name = "v2Challenge-CreateLambda-" + salt

    # Create IAM role
    role_arn = create_iam_role(role_name)
    if role_arn:
        # Create Lambda function
        function_arn = create_lambda_function(function_name, role_arn)
        if function_arn:
            # Give some time for Lambda function to be fully set up
            time.sleep(10)
            # Invoke Lambda function
            invoke_lambda_function(function_name)
