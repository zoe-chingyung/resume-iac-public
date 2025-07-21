import json
import base64
import boto3
import os
import logging
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event, default=str)}")
    
    s3 = boto3.client('s3')
    # Use environment variables for flexibility
    bucket = os.environ.get('RESUME_BUCKET', 'ching-resume-html')
    key = os.environ.get('RESUME_KEY', 'resume.pdf')
    
    try:
        logger.info(f"Fetching PDF from S3 bucket: {bucket}, key: {key}")
        response = s3.get_object(Bucket=bucket, Key=key)
        pdf_data = response['Body'].read()
        logger.info(f"Fetched PDF size: {len(pdf_data)} bytes")
        
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        logger.info(f"Base64-encoded PDF length: {len(pdf_base64)} characters")
        
        # Log a short sample for debugging
        logger.info(f"Base64 sample: {pdf_base64[:60]}...")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'inline; filename=resume.pdf',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': pdf_base64,
            'isBase64Encoded': True
        }
        
    except ClientError as e:
        logger.error(f"S3 error: {str(e)}")
        return {
            'statusCode': 404 if e.response['Error']['Code'] == 'NoSuchKey' else 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'PDF not found' if e.response['Error']['Code'] == 'NoSuchKey' else 'Failed to fetch PDF',
                'message': str(e)
            })
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }