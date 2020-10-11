import json
import boto3
import os

# Get the service resource
sqs = boto3.resource('sqs')

queue_name = os.environ['SQS_QUEUE']
queue_url = os.environ['SQS_URL']

# Get the queue
queue = sqs.get_queue_by_name(QueueName=queue_name)


def lambda_handler(event, context):
    # Send message to SQS:
    response = queue.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(json.loads(event['body']))
    )

    return {
        'statusCode': 200,
        'body': 'OK'
    }