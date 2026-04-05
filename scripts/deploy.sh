#!/bin/bash
# scripts/deploy.sh

# Build the application
sam build

# Deploy to AWS
sam deploy \
  --template-file infrastructure/template.yaml \
  --stack-name ecommerce-backend \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    AdminEmail=omarfesal4296@gmail.com \
    FromEmail=noreply@example.com \
  --s3-bucket=dev-ecommerce-products-747639504940 \
  --no-resolve-s3 \
  --tags Project=ECommerce Environment=Production

# Get outputs
aws cloudformation describe-stacks \
  --stack-name ecommerce-backend \
  --query 'Stacks[0].Outputs' \
  --output table