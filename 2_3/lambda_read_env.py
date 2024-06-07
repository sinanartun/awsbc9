
import os

def lambda_handler(event, context):

    secret = os.environ.get('SECRET')
    
    if not secret:
        return {
            'statusCode': 500,
            'body': 'SECRET environment variable not set'
        }
    
    try:

        return {
            'statusCode': 200,
            'body': secret 
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
