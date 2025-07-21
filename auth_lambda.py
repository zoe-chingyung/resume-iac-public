import json
import boto3
import os
import logging
import requests
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global variable to cache password (avoid calling SSM every time)
cached_password = None

def get_password():
    global cached_password
    if cached_password is not None:
        logger.info("Using cached password")
        return cached_password
    
    try:
        logger.info("Fetching password from SSM")
        ssm = boto3.client('ssm')
        response = ssm.get_parameter(
            Name=os.environ['PARAMETER_NAME'], 
            WithDecryption=True
        )
        cached_password = response['Parameter']['Value']
        logger.info("Password fetched and cached successfully")
        return cached_password
    except ClientError as e:
        logger.error(f"Failed to fetch password from SSM: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching password: {str(e)}")
        raise

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event, default=str)}")
    
    headers = {
        "Access-Control-Allow-Origin": "https://chingyung.uk",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST,OPTIONS"
    }

    # Handle preflight OPTIONS request
    if event.get('httpMethod') == 'OPTIONS':
        logger.info("Handling CORS preflight request")
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight OK"})
        }

    try:
        body = json.loads(event.get('body', '{}'))
        input_password = body.get('password', '')

        # Extract IP and user agent
        ip = event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown')
        user_agent = event.get('requestContext', {}).get('identity', {}).get('userAgent', 'unknown')

        # Call GeoIP API
        try:
            geo_resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
            geo_data = geo_resp.json() if geo_resp.status_code == 200 else {}
            location = f"{geo_data.get('country', 'unknown')} - {geo_data.get('regionName', '')} - {geo_data.get('city', '')}"
        except Exception as e:
            logger.warning(f"GeoIP lookup failed for IP {ip}: {str(e)}")
            location = "GeoIP lookup failed"

        # Log user info
        logger.info(f"[REQUEST INFO] IP: {ip} | Location: {location} | User-Agent: {user_agent} | Input password: {input_password[:3]}***")

        correct_password = get_password()
        
        if input_password != correct_password:
            logger.info("Password mismatch")
            return {
                "statusCode": 401,
                "headers": headers,
                "body": json.dumps({"message": "Unauthorized"})
            }
        
        logger.info("Password correct, generating presigned URL")
        
        s3 = boto3.client('s3')
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': os.environ['BUCKET_NAME'], 
                'Key': 'index.html'
            },
            ExpiresIn=int(os.environ['EXPIRATION'])
        )
        
        logger.info("Presigned URL generated successfully")
        
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "Auth successful",
                "url": url
            })
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"message": "Invalid request body"})
        }
    except ClientError as e:
        logger.error(f"AWS service error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": "Service temporarily unavailable"})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": "Internal server error"})
        }
