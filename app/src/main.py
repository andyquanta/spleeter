# Initialize the fastapi app
import signal

from fastapi import FastAPI
import concurrent.futures
from contextlib import asynccontextmanager
from service.pub_sub import start_pubsub_listener
from service.pub_sub import stop_event


def signal_handler(sig, frame):
    print("Signal received, shutting down...")
    stop_event.set()


# Initialize a background task to listen to pubsub messages
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the Pub/Sub listener in the background
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.submit(start_pubsub_listener)
        yield
        stop_event.wait()
        yield
        


app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)