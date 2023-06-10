#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

from drive_classes import *

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

creds = DriveApp.returnCreds()

try:
    service = build('drive', 'v3', credentials=creds)
    
    folder_metadata = {
        "name": "Test",
        "mimeType": "application/vnd.google-apps.folder"
    }

    folder = service.files().create(body=folder_metadata, fields="id").execute()
    print(f'File ID: {folder.get("id")}')

except HttpError as error:
    print(f'An error occurred: {error}')