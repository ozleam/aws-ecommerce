# services/orders/order_worker.py
import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')
stepfunctions = boto3.client('stepfunctions')

def lambda_handler(event, context):
    for record in event['Records']:
        order = json.loads(record['body'])

        try:
            # Process order
            order['status'] = 'PROCESSING'
            order['processedAt'] = datetime.utcnow().isoformat()

            # Start Step Functions workflow
            stepfunctions.start_execution(
                stateMachineArn=os.environ['STATE_MACHINE_ARN'],
                input=json.dumps(order),
                name=f"order-{order['orderId']}"
            )

            # Update order status
            table.update_item(
                Key={'orderId': order['orderId']},
                UpdateExpression='SET #status = :status, processedAt = :processedAt',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': 'PROCESSING',
                    ':processedAt': order['processedAt']
                }
            )

        except Exception as e:
            print(f"Error processing order {order['orderId']}: {str(e)}")
            # Will retry automatically based on visibility timeout
            raise e

    return {'statusCode': 200}