#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details. 
# Further see 'Apache 2.0 clause 4' in the LICENSE.md file in the project root
#
# Copyright 2018 Google LLC
# Licensed under the Apache 2.0 license. See LICENSE.md file in the project root for details.
#
# In compliance with the Apache 2.0 license Google used to license their code, I have made clear of 
# what changes I have made to their code.
# Source code: https://github.com/googleworkspace/python-samples/blob/main/drive/quickstart/quickstart.py
#

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.install',
    'https://www.googleapis.com/auth/drive'
]

def requestCreds():
    # code licensed by Google starts here
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # I removed a comment, added a line, and put this next if statment to be under "if os.path.exists('token.json'):"
        if not creds or not creds.valid:
            if creds and creds and creds.refresh_token:
                creds.refresh(Request())
    # I have moved this next else statement to not by under "if creds and creds and creds.refresh_token:"
    else: 
        flow = InstalledAppFlow.from_client_secrets_file(
            # renamed 'credentials.json' to 'drive-credentials.json'
            'drive-credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    # code licensed by Google stops here

    return creds
    
if __name__ == "__main__":
    requestCreds()