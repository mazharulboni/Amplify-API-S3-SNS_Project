import json
import boto3
import os

def lambda_handler(event, context):
    # Retrieve the S3 bucket and key information from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Create an SES client
    ses_client = boto3.client('ses')

    # Specify the sender and recipient email addresses
    sender_email = os.environ['SenderEmail']
    recipient_email = os.environ['RecipientEmail']

    # Construct the email message
    subject = 'New image upload'
    body_text = 'An image has been uploaded to the S3 bucket.'
    body_html = '<p>An image has been uploaded to the S3 bucket.</p>'
    attachment_name = key.split('/')[-1]  # Use the image filename as the attachment name

    # Create the email message
    email_message = {
        'Subject': {'Data': subject},
        'Body': {
            'Text': {'Data': body_text},
            'Html': {'Data': body_html}
        },
        'Source': sender_email,
        'Destination': {'ToAddresses': [recipient_email]}
    }

    # Add the image as an attachment
    attachment = {
        'Data': get_s3_object(bucket_name, key),
        'FileName': attachment_name
    }
    email_message['Attachments'] = [attachment]

    # Send the email
    response = ses_client.send_email(EmailMessage=email_message)

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully')
    }

def get_s3_object(bucket_name, key):
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Retrieve the object from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    return response['Body'].read()
