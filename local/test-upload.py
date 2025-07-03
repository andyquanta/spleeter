import requests
import os

signed_url = 'https://storage.googleapis.com/audition-toolkit.appspot.com/audition-app-files/17f61250-450f-45ac-9f27-92f1b66f6339.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=storage-saver%40audition-toolkit.iam.gserviceaccount.com%2F20240908%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240908T164935Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host%3Bx-goog-resumable&X-Goog-Signature=5955a6eeef4be9433840af4fc0c65752e2afed255255fcf37f71c1806570b12680d835f227a5a8332da8166d50060c4ac86e1d8a6902e5cca27556ad2b1f488b2b65df873aa9551e60bd78aadab277841e41334aa69165ea7004dc980339940b47f139b512dc362aec2d129c58c76cf89ac1262c7803d27e4aef5d4fba67757562ff39dda08663026fae3944e0d248b34a8e5e35b19bc949edf4cd21f2efac378c390bdf7266493aa31ab432bedefcb5c36631288805681c2c5152478abc0aabb72537859b3da11a1098aa5862b3f07fb62d0707522b2464f484abeefc9aba780ff9bf1ad771631edb1bc9d9b22479e0ff4faa9c690451abaa5c42ccf139d70e'


# Upload file in chunks (set chunk size as per your needs)
chunk_size = 1024 * 1024  # 1MB

def upload_chunk(upload_url, file_path, start, chunk):
    total_size = os.path.getsize(file_path)
    headers = {
        'Content-Range': f'bytes {start}-{start + len(chunk) - 1}/{total_size}'
    }
    response = requests.put(upload_url, headers=headers, data=chunk)

    if response.status_code in [200, 201, 308]:
        # 308 indicates that the upload is incomplete, but the chunk was successfully uploaded
        return True
    else:
        print(f"Failed to upload chunk: {response.text}")
        return False




# Initiate the resumable upload session
headers = {
    'x-goog-resumable': 'start',
    'Content-Type': 'application/zip'  # Specify the content type of the file
}

response = requests.post(signed_url, headers=headers)

# The response will contain a session URL in the "Location" header
if response.status_code == 201:
    upload_url = response.headers['Location']
    print(f"Resumable session started: {upload_url}")
    # Read the file and upload in chunks
    file_path = "8904bb40-acf0-41db-971d-324d4abd54a6.zip"
    with open(file_path, 'rb') as f:
        start = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            success = upload_chunk(upload_url, file_path, start, chunk)
            if not success:
                break
            start += len(chunk)

    print("File upload completed.")
else:
    print(f"Failed to start resumable upload session: {response.text}")


