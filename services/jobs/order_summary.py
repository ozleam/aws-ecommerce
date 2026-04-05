# services/jobs/order_summary.py
import json
import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('orders')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Get yesterday's orders
    yesterday = datetime.utcnow() - timedelta(days=1)

    # Scan orders from last 24 hours
    response = orders_table.scan()

    total_orders = 0
    total_revenue = 0
    orders_by_status = {}

    for order in response['Items']:
        order_date = datetime.fromisoformat(order['createdAt'])
        if order_date > yesterday:
            total_orders += 1
            total_revenue += order['total']
            status = order['status']
            orders_by_status[status] = orders_by_status.get(status, 0) + 1

    # Send summary report
    summary = f"""
    Daily Order Summary:
    Date: {datetime.utcnow().date()}
    Total Orders: {total_orders}
    Total Revenue: ${total_revenue}
    Status Breakdown: {json.dumps(orders_by_status)}
    """

    sns.publish(
        TopicArn=os.environ['REPORT_TOPIC_ARN'],
        Subject='Daily Order Summary',
        Message=summary
    )

    return {'statusCode': 200}