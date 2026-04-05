# services/auth/authorizer.py
import json
import jwt
import os

def lambda_handler(event, context):
    token = event['authorizationToken'].split(' ')[1]

    try:
        # Verify JWT token
        decoded = jwt.decode(
            token,
            algorithms=['RS256'],
            options={'verify_aud': False}
        )

        return {
            'principalId': decoded['sub'],
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [{
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Allow',
                    'Resource': event['methodArn']
                }]
            },
            'context': {
                'userId': decoded['sub'],
                'email': decoded['email']
            }
        }
    except Exception as e:
        raise Exception('Unauthorized')