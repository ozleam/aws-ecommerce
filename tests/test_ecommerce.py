# tests/test_ecommerce.py
import requests
import boto3

def test_workflow():
    # 1. Register user
    cognito = boto3.client('cognito-idp')
    response = cognito.sign_up(
        ClientId='your-client-id',
        Username='test@example.com',
        Password='Test123!@#',
        UserAttributes=[{'Name': 'email', 'Value': 'test@example.com'}]
    )

    # 2. Login
    auth_response = cognito.initiate_auth(
        ClientId='your-client-id',
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': 'test@example.com',
            'PASSWORD': 'Test123!@#'
        }
    )
    token = auth_response['AuthenticationResult']['AccessToken']

    # 3. Add product
    api_url = 'https://your-api-id.execute-api.region.amazonaws.com/prod'
    headers = {'Authorization': f'Bearer {token}'}

    product = {
        'name': 'Test Product',
        'price': 29.99,
        'description': 'Test Description',
        'category': 'Electronics',
        'stock': 100
    }

    response = requests.post(
        f'{api_url}/products',
        json=product,
        headers=headers
    )

    # 4. Place order
    order = {
        'items': [{'productId': 'test-id', 'quantity': 2}],
        'total': 59.98,
        'paymentMethod': 'credit_card'
    }

    response = requests.post(
        f'{api_url}/orders',
        json=order,
        headers=headers
    )

    print(f"Order placed: {response.json()}")

    # 5. Check order status
    order_id = response.json()['orderId']
    response = requests.get(
        f'{api_url}/orders/{order_id}',
        headers=headers
    )

    print(f"Order status: {response.json()}")