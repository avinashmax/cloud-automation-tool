import boto3

# Create an STS client
sts_client = boto3.client('sts')

# Get AWS account details
response = sts_client.get_caller_identity()

print("✅ Connected to AWS successfully!")
print("Account ID:", response['Account'])
print("User ARN:", response['Arn'])
