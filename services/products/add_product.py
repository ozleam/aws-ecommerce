# services/products/add_product.py
import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('products')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    product_id = str(uuid.uuid4())

    product = {
        'productId': product_id,
        'name': body['name'],
        'price': float(body['price']),
        'description': body['description'],
        'category': body['category'],
        'stock': int(body['stock']),
        'createdAt': datetime.utcnow().isoformat()
    }

    table.put_item(Item=product)

    # Generate pre-signed URL for image upload
    image_key = f"products/{product_id}/image.jpg"
    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': os.environ['PRODUCTS_BUCKET'],
            'Key': image_key,
            'ContentType': 'image/jpeg'
        },
        ExpiresIn=3600
    )

    return {
        'statusCode': 201,
        'body': json.dumps({
            'productId': product_id,
            'product': product,
            'uploadUrl': presigned_url
        })
    }