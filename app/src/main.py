# Initialize the fastapi app
import signal

import logging

from fastapi import FastAPI, BackgroundTasks
from fastapi import Path, Header
import concurrent.futures
from contextlib import asynccontextmanager
from service import file_processor
from service import publish_notification
import asyncio
#from service.pub_sub import start_pubsub_listener
#from service.pub_sub import stop_event

logging.basicConfig(level=logging.INFO)


app = FastAPI(docs_url="/karaoke/docs", redoc_url=None, openapi_url="/karaoke/openapi.json")

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