# services/orders/place_order.py
import json
import boto3
import os
from datetime import datetime

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_id = event['requestContext']['authorizer']['claims']['sub']

    order = {
        'orderId': str(uuid.uuid4()),
        'userId': user_id,
        'items': body['items'],
        'total': body['total'],
        'status': 'PENDING',
        'createdAt': datetime.utcnow().isoformat()
    }

    # Save to DynamoDB
    table.put_item(Item=order)

    # Send to SQS for async processing
    sqs.send_message(
        QueueUrl=os.environ['ORDER_QUEUE_URL'],
        MessageBody=json.dumps(order),
        MessageAttributes={
            'orderType': {
                'DataType': 'String',
                'StringValue': body.get('type', 'standard')
            }
        }
    )

    return {
        'statusCode': 202,
        'body': json.dumps({
            'message': 'Order received',
            'orderId': order['orderId'],
            'status': 'PENDING'
        })
    }