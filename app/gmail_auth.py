from __future__ import print_function
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail modify scope (safe)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

TOKEN_PATH = "token.pickle"
CREDENTIALS_PATH = "credentials.json"


def get_gmail_credentials():
    creds = None

    # Load existing token
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    # If token missing or expired, log in again
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    "credentials.json not found in project root"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save token
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return creds