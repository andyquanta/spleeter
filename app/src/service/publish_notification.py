import firebase_admin
from firebase_admin import messaging
import os
import asyncio

# Initialize the Firebase Admin SDK
firebase_cred_path = os.getenv('FIREBASE_CRED_PATH', '/key/notification-svc.json')
credentials = firebase_admin.credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(credentials)

async def send_notification(device_token, message_title, message_body):
    print(f"Sending notification to device: {device_token}")
    # Create a message
    message = messaging.Message(
        data={
            'title': message_title,
            'file': message_body,
        },
        token=device_token,
    )

    # Send the message
    response = asyncio.run(messaging.send(message))
    print('Successfully sent message:', response)

# Example usage

#send_notification(user_device_token, 'File Ready for Download', 'Your audio file is now ready for download.')
