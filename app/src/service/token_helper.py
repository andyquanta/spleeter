import jwt
from jwt import InvalidTokenError
import os
import base64
import json
from fastapi import HTTPException
import logging

jwt_secret = os.getenv("JWT_SECRET")

def parse_jwt_header(encoded_jwt):
    
    # Split the JWT into its components
    header_b64, _, _ = encoded_jwt.split('.')
    
    # Add necessary padding to the base64 encoded header
    header_b64 += '=' * (-len(header_b64) % 4)
    
    # Decode the base64 encoded header
    header_json = base64.urlsafe_b64decode(header_b64).decode('utf-8')
    
    # Parse the JSON header
    header = json.loads(header_json)
    
    return header

def validate_jwt(encoded_jwt, secret_key=jwt_secret, algorithms=['RS256']):
    try:
        # Decode and validate the JWT
        logging.info(f"encoded JWT {encoded_jwt} secret key {secret_key} algorithms {algorithms}")        
        decoded_jwt = jwt.decode(encoded_jwt, secret_key, algorithms=algorithms)
        return decoded_jwt
    except InvalidTokenError as e:
        # Handle invalid token errors
        print(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
