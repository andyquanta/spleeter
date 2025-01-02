# Download file from GCS
import os
import asyncio
import datetime
import sys


from google.cloud import storage
from google.oauth2 import service_account

from service.publish_notification import send_notification
from service import token_helper

SERVICE_ACCOUNT_FILE = os.getenv("STORAGE_KEY", "/key/storage.json")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

BUCKET_NAME = os.getenv("BUCKET_NAME", "audition-toolkit.appspot.com")
BASE_PATH = os.getenv("BASE_PATH", "audition-app-files")
DEST_PATH = os.getenv("DEST_PATH", "/raw")


async def download_file(source_blob_name, destination_file_name):
    print(f"Downloading file... {source_blob_name} to {destination_file_name}")
    """Downloads a blob from the bucket."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(source_blob_name)
    print(f"file downloading started {blob}")
    await asyncio.to_thread(blob.download_to_filename, destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")


async def unzip_with_native(zip_file, extract_to):
    print(f"Unzipping file {zip_file} to {extract_to}")
    # Unzip the file using subprocess in async
    process = await asyncio.create_subprocess_shell(f"unzip {zip_file} -d {extract_to}")
    await process.wait()

async def zip_with_native(file_name, zip_file):
    print(f"Zipping file {file_name} to {zip_file}")
    # Zip the file using subprocess in async
    process = await asyncio.create_subprocess_shell(f"zip -r {zip_file} {file_name}")
    await process.wait()

async def apply_karaoke(folder_name):
    print(f"Applying karaoke effect to folder name {folder_name}")
    # Get the first file in folder
    file_name = os.listdir(folder_name)[0]
    # Apply karaoke effect to the audio file
    spleeter_cmd = f"spleeter separate -o {folder_name}/output -c mp3 -f {{instrument}}.{{codec}} \
        -p spleeter:2stems {folder_name}/{file_name}"
    print(f"Running command: {spleeter_cmd}")
    process = await asyncio.create_subprocess_shell(
        f"{spleeter_cmd}"
    )
    await process.wait()
    return f"{folder_name}/output/accompaniment.mp3"


async def cleanup(file_name):
    print(f"Cleaning up {file_name}...")
    # Remove the file after processing
    await asyncio.create_subprocess_shell(f"rm -rf {file_name}")


async def upload_file(source_file_name, destination_blob_name):
    print(f"Uploading file... {source_file_name} to {destination_blob_name}")
    """Uploads a file to the bucket."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    await asyncio.to_thread(blob.upload_from_filename, source_file_name)
    signed_url = asyncio.to_thread(
        blob.generate_signed_url,
        version="v4",
        expiration=datetime.timedelta(minutes=180),
        method="GET",
    )

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    return signed_url


async def process_file(source_file_name: str, jwt_token: str, device_token: str):

    token_helper.validate_jwt(jwt_token)
    file_to_download = f"{BASE_PATH}/{source_file_name}"
    await download_file(file_to_download, f"{DEST_PATH}/{source_file_name}")
    downloaded_file = f"{DEST_PATH}/{source_file_name}"
    folder_name = source_file_name.split(".")[0]
    extracted_folder = f"{DEST_PATH}/{folder_name}"
    await unzip_with_native(downloaded_file, extracted_folder)
    accompaniment_file = await apply_karaoke(extracted_folder)
    final_zip_file = f"{extracted_folder}/output/{folder_name}.zip"
    await zip_with_native(f"{accompaniment_file}", f"{final_zip_file}")
    signed_url = await upload_file(f"{final_zip_file}", f"{BASE_PATH}/instruments/{folder_name}.zip")

    await send_notification(device_token, "Your Karaoke File is ready for download", f"{signed_url}")
    #await cleanup(source_file_name.split(".")[0])

    print(f"File {source_file_name} processed")
