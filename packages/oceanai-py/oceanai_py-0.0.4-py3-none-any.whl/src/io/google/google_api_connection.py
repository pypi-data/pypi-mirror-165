from http import client
from typing import List
import fs
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google

class GoogleCredentials():
    
    def __init__(self) -> None:
        self.client_id = ""
        self.cliente_secret = ""
        self.redirect_uris = []
        

class GoogleAPIConnector():
    
    def __init__(self,tokenPath:str,scope:List) -> None:
        self.tokenPath = tokenPath
        self.scope = scope
        self.auth = None
        
    def autorize(self, credentials:GoogleCredentials):
        oAuth2Client = google.auth.OAuth2(
                credentials.client_id, credentials.client_secret, credentials.redirect_uris[0]
            )
        if os.path.exists(self.tokenPath):
            creds = Credentials.from_authorized_user_file(self.tokenPath, self.scope)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                                'credentials.json', self.scope)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(self.tokenPath, 'w') as token:
                    token.write(creds.to_json())
            else:
                self.auth = oAuth2Client