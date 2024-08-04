import os
import json
import asyncio
import threading
import time

from google.cloud import pubsub_v1

from google.oauth2 import service_account
from service.file_processor import process_file

stop_event = threading.Event()

# Google Cloud Pub/Sub configuration
SERVICE_ACCOUNT_FILE = os.getenv("PUBSUB_KEY", "/key/pub-sub.json")

# Your Google Cloud Project ID and Pub/Sub topic
PROJECT_ID = "audition-toolkit"
# TOPIC_NAME = "projects/audition-toolkit/topics/main-file-topic"
TOPIC_NAME = "main-file-topic"

SUBSCRIPTION_NAME = "main-file-topic-sub"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Initialize Pub/Sub subscriber
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)

# Callback function to process messages
def callback(message):
    message_content: str = message.data.decode('utf-8')
    print(f"Received message: {message_content} type: {type(message_content)}")
    try:
        message_json = json.loads(message_content)
        file_name = message_json["data"]["file_name"]
        print(f"Processing file: {file_name}")
        # run process_file hich is coroutine in a blocking way
        asyncio.run(process_file(file_name))

        
    except Exception as e:
        # print stack trace
        print(e.with_traceback())
        print(f"Error processing message: {e}")
        exit(1)
    message.ack()

# Background task to listen for Pub/Sub messages
def start_pubsub_listener():
    global stop_event
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    with subscriber:
        try:
            print("listener try")
            while not stop_event.is_set():
                print("listener while")
                time.sleep(1)
            exit(0)
            #streaming_pull_future.cancel()
            
            # streaming_pull_future.result()
        except Exception as e:
            print(f"Listening for messages on {subscription_path} threw an exception: {e}.")
            streaming_pull_future.cancel()

