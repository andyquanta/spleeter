# Download file from GCS
import os
import asyncio


from google.cloud import storage
from google.oauth2 import service_account

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
    # Unzip the file using subprocess in async
    await asyncio.create_subprocess_shell(f"unzip {zip_file} -d {extract_to}")


async def apply_karaoke(folder_name):
    print(f"Applying karaoke effect to folder name {folder_name}")
    # Get the first file in folder
    file_name = os.listdir(folder_name)[0]
    # Apply karaoke effect to the audio file
    await asyncio.create_subprocess_shell(f"spleeter separate -i {folder_name}/{file_name} -o output {folder_name}/output")

    
async def cleanup(file_name):
    print(f"Cleaning up {file_name}...")
    # Remove the file after processing
    await asyncio.create_subprocess_shell(f"rm -rf {file_name}")



async def process_file(source_file_name: str):
    file_to_download = f"{BASE_PATH}/{source_file_name}"
    await download_file(file_to_download, f"/{DEST_PATH}/{source_file_name}")
    downloaded_file = f"{DEST_PATH}/{source_file_name}"
    folder_name = source_file_name.split(".")[0]
    extracted_folder = f"{DEST_PATH}/{folder_name}"
    await unzip_with_native(downloaded_file, extracted_folder)
    await apply_karaoke(extracted_folder)
    #await cleanup(source_file_name.split(".")[0])
    

    print(f"File {source_file_name} processed")