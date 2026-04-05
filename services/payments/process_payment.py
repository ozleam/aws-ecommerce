# services/payments/process_payment.py
import json
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    order = event

    # Simulate payment processing
    payment_amount = order['total']
    payment_method = order.get('paymentMethod', 'credit_card')

    # Store payment info in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    payment_table = dynamodb.Table('payments')

    payment = {
        'paymentId': str(uuid.uuid4()),
        'orderId': order['orderId'],
        'amount': payment_amount,
        'method': payment_method,
        'status': 'SUCCESS' if payment_amount <= 10000 else 'FAILED',
        'processedAt': datetime.utcnow().isoformat()
    }

    payment_table.put_item(Item=payment)

    if payment['status'] == 'FAILED':
        raise Exception('PaymentFailedException')

    return {
        'orderId': order['orderId'],
        'paymentId': payment['paymentId'],
        'status': 'PAID'
    }