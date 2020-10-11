import boto3
from dotenv import load_dotenv
import time
import json
import requests
import datetime
import os

load_dotenv()


class SqsListener:
    def __init__(self, queue_name):
        self.queue_name = queue_name

    def get_queue(self):
        sqs = boto3.resource('sqs')
        return sqs.get_queue_by_name(QueueName=self.queue_name)

    def get_messages(self):
        return self.get_queue().receive_messages()

    def process_messages(self, with_class=None):
        for message in self.get_messages():
            if with_class is not None:
                processor = with_class(message)
                if processor.validate():
                    if processor.execute() is False:
                        processor.fail()
            self.delete_message(message)

    def delete_message(self, message):
        message.delete()


class SqsProcessor:
    def __init__(self, message):
        try:
            self.raw_message = message
            self.parsed_message = self.deserialize(message.body)
        except:
            self.raw_message = ''
            self.parsed_message = ''

    def deserialize(self, body):
        return json.loads(body)

    def validate(self):
        return True

    def execute(self):
        return True

    def fail(self):
        pass


class LocalWebsitePassThrough(SqsProcessor):
    def validate(self):
        return True

    def execute(self):
        received_time = datetime.datetime.now().strftime("%I:%M%p")
        request_type = self.parsed_message.get('type')
        try:
            response = requests.post(os.getenv('DESTINATION_URL'), None, self.parsed_message)
            print('[' + received_time + '] Request Type - ' + str(request_type) + ' --> Response: ' + str(response.content))
        except Exception as e:
            print('[' + received_time + '] Request Type - ' + str(request_type) + ' --> Error: ' + str(e))


if __name__ == '__main__':
    while True:
        listener = SqsListener(os.getenv('SQS_QUEUE'))
        listener.process_messages(LocalWebsitePassThrough)
        time.sleep(float(os.getenv('POLL_DELAY')))
