# services/notifications/send_notification.py
import json
import boto3
import os

ses = boto3.client('ses')
sns = boto3.client('sns')

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # Send email via SES
    email_response = ses.send_email(
        Source=os.environ['SES_FROM_EMAIL'],
        Destination={
            'ToAddresses': [message['userEmail']]
        },
        Message={
            'Subject': {
                'Data': f"Order {message['status']} - #{message['orderId']}"
            },
            'Body': {
                'Html': {
                    'Data': f"""
                    <h1>Order {message['status']}</h1>
                    <p>Order ID: {message['orderId']}</p>
                    <p>Total: ${message['total']}</p>
                    <p>Status: {message['status']}</p>
                    """
                }
            }
        }
    )

    # Send SMS via SNS (optional)
    if 'phoneNumber' in message:
        sns.publish(
            PhoneNumber=message['phoneNumber'],
            Message=f"Order {message['orderId']} is {message['status']}"
        )

    return {
        'statusCode': 200,
        'body': json.dumps({'messageId': email_response['MessageId']})
    }