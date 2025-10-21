# Initialize the fastapi app
import os
import signal

import logging
import base64
import json

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi import Path, Header
import concurrent.futures
from contextlib import asynccontextmanager
from service import file_processor
from service import publish_notification
import asyncio
from service.pub_sub import start_pubsub_listener
#from service.pub_sub import stop_event

logging.basicConfig(level=logging.INFO)


app = FastAPI(docs_url="/karaoke/docs", redoc_url=None, openapi_url="/karaoke/openapi.json")

ENABLE_PUBSUB_LISTENER = os.getenv("ENABLE_PUBSUB_LISTENER", "false").lower() == "true"

#Run Pub/Sub listener in background on startup
@app.on_event("startup")
async def startup_event():
    if not ENABLE_PUBSUB_LISTENER:
        logging.info("Pub/Sub listener is disabled.")
        return
    logging.info("Starting Pub/Sub listener in background...")
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_pubsub_listener)


@app.get("/karaoke/health")
async def health():
    return {"status": "ok"}


@app.post("/karaoke/file/{file_id}/process")
async def process_karaoke(file_id: str = Path(title="File ID", description="Unique file ID"),
                          jwt_token: str = Header(default=None, title="JWT Token", description="JWT Token"),
                          device_token: str = Header(default=None, title="Device Token", description="Device Token"),
                          background_tasks: BackgroundTasks = None
                          ):
    logging.info(f"Processing file {file_id} with JWT token {jwt_token} and device token {device_token}")
    background_tasks.add_task(file_processor.process_file, file_id, jwt_token, device_token)

    return {"status": "processing", "file_id": file_id}


@app.post("/karaoke/file/message")
async def send_message(device_token: str = Header(default=None, title="Device Token", description="Device Token"),
                       message_title: str = Header(default=None, title="Message Title", description="Message Title"),
                       message_body: str = Header(default=None, title="Message Body", description="Message Body"),
                       ):
    
    await publish_notification.send_notification(device_token, message_title, message_body)

    return {"status": "sending", "device_token": device_token}


@app.post("/karaoke/process")
async def process_karaoke(request: dict, background_tasks: BackgroundTasks = None):
    logging.info(f"Received request to process karaoke file {dict}")
    #print all key value pairs in the dictionary including nested dictionaries
    def print_dict(d, parent_key=''):
        for key, value in d.items():
            if isinstance(value, dict):
                print_dict(value, parent_key + key + '.')
            else:
                logging.info(f"Key: {parent_key + key}, Value: {value}")

    print_dict(request)

    encoded_data = request["message"]["data"]
    if(encoded_data is None):
        logging.error("No data found in the request message")
        raise HTTPException(status_code=400, detail="No data found in the request message")
    #decode the base64 encoded data
    decoded_bytes = base64.b64decode(encoded_data)
    decoded_str = decoded_bytes.decode('utf-8')
    # parse the json string

    data_container = json.loads(decoded_str)
    logging.info(f"Decoded data: {data_container}")
    data = data_container.get("data")
    file_id = data.get("file_id")
    jwt_token = data.get("jwt_token")
    device_token = data.get("device_token")

    logging.info(f"Processing file {file_id} with JWT token {jwt_token} and device token {device_token}")
    background_tasks.add_task(file_processor.process_file, file_id, jwt_token, device_token)

    return {"status": "processing", "file_id": file_id}