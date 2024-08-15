import time
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def get_token():
    if os.path.exists('token.json'):
        SCOPES = ["https://www.googleapis.com/auth/forms.body", "https://www.googleapis.com/auth/forms.responses.readonly"]
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if creds.expiry and time.time() >= creds.expiry.timestamp():
            if creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open('token.json', 'w') as token_file:
                        token_file.write(creds.to_json())
                    print("Credentials have been refreshed.")
                except Exception as e:
                    print(f"Failed to refresh token: {e}")
                    return None
            else:
                print("Credentials are invalid and cannot be refreshed.")
                return None
        return creds
    else:
        print('No valid credentials found. Please follow the authorization steps.')
        return None
