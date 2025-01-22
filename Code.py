import boto3
import datetime
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
appsync_client = boto3.client('appsync')
sns_client = boto3.client('sns')

# Constants
SNS_TOPIC_ARN = '##########################'  # Replace with your SNS Topic ARN
NOTIFY_BEFORE_DAYS = 15  # Notify if the API key expires within these days
APPSYNC_API_ID = '###########################'  # Replace with your AppSync API ID
TARGET_API_KEY_ID = '##########################'  # Replace with your specific AppSync API key ID

def lambda_handler(event, context):
    try:
        # Fetch API keys
        logger.info("Fetching API keys for AppSync API ID: %s", APPSYNC_API_ID)
        response = appsync_client.list_api_keys(apiId=APPSYNC_API_ID)
        now = datetime.datetime.now(datetime.timezone.utc)

        # Find the target API key
        target_key = next((key for key in response['apiKeys'] if key['id'] == TARGET_API_KEY_ID), None)

        if not target_key:
            logger.error("API key with ID %s not found.", TARGET_API_KEY_ID)
            return {
                'statusCode': 404,
                'body': f"API key with ID {TARGET_API_KEY_ID} not found."
            }

        # Check expiry date
        expiry_date = datetime.datetime.fromtimestamp(target_key['expires'], tz=datetime.timezone.utc)
        days_to_expiry = (expiry_date - now).days
        logger.info("API key %s expires on %s (%d days remaining).", TARGET_API_KEY_ID, expiry_date.isoformat(), days_to_expiry)

        # Send notification if the key is close to expiry
        if days_to_expiry <= NOTIFY_BEFORE_DAYS:
            message = (
                f"The AppSync API key with ID {TARGET_API_KEY_ID} is about to expire.\n\n"
                f"Expiry Date: {expiry_date.isoformat()}\n"
                f"Days to Expiry: {days_to_expiry} days\n"
            )
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="AppSync API Key Expiry Notification",
                Message=message
            )
            logger.info("Notification sent for API key %s.", TARGET_API_KEY_ID)
            return {
                'statusCode': 200,
                'body': f"Notification sent for API key {TARGET_API_KEY_ID}."
            }

        return {
            'statusCode': 200,
            'body': f"API key {TARGET_API_KEY_ID} is not close to expiry ({days_to_expiry} days remaining)."
        }

    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }
