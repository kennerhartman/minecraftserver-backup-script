#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

import dropbox
import subprocess
from decouple import config 

# my own JSON module that creates, reads, and writes to JSON files
from dbxJSON import InteractJSON

# because of security reasons, 'dbx-credentials.json' is in my '.gitignore'.  
# if this JSON is not present, then one will be created with the needed data to authenticate with Dropbox
data = {
    "retrieved_token": False,
    "generated_access_code": None,
    "access_token": None,
    "refresh_token": None
}

InteractJSON.createFile(data)
settings = InteractJSON.readFile()

# to make things more convenient, 'dbx.py' will automatically run 'dbx-auth.py'
# to retrieve access and refresh tokens, as well as generating an access code 
# and storing them in 'dbx-credentials.json'
if (settings['retrieved_token'] == False):
    subprocess.call(['python3', 'dbx-auth.py'])
else:
    print("You are already authenticated with the Dropbox API.  If you want to refresh any token, run 'dbx-auth.py'.\n")

# ============= # ============= #

# grab app key and secrets from '.env'
APP_KEY = config("APP_KEY")

# read every key in dbx-credentials.json
auth = InteractJSON.readFile()

# initialize Dropbox API
dbx = dropbox.Dropbox(
    app_key=APP_KEY,
    oauth2_refresh_token=auth['refresh_token']
)

# ============= # ============= #

"""
In another .py file, create a class that will have the following functions:

- checking if a specifically named folder is present
- handle uploading world-backup to Dropbox
- other functions that may be needed...
"""

