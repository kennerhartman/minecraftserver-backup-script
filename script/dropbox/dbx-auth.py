#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

import dropbox
import time
from decouple import config
import webbrowser

# my own JSON module that creates, reads, and writes to JSON files
from dbxJSON import InteractJSON

APP_KEY = config("APP_KEY")

try:
    settings = InteractJSON.readFile()
except:
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

def redirectTime():
    for i in range(5, 0, -1):
        print("You will be redirected in (" + str(i) + ")")
        time.sleep(1)
        print ("\033[A\033[A")

# source: https://github.com/dropbox/dropbox-sdk-python/blob/main/example/oauth/commandline-oauth-pkce.py
auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')

authorize_url = auth_flow.start()

print("\nBeginning authentication...\n")

print("1. When redirected, click \"Continue\", then \"Allow\" (you might have to log in first).")
print("2. Copy the authorization code.\n")

redirectTime()
webbrowser.open(authorize_url)

auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
    
    # store auth code and oauth results into dbx-crednetials.json
    access_token = oauth_result.access_token
    refresh_token = oauth_result.refresh_token

    settings["generated_access_code"] = auth_code
    settings["access_token"] = access_token
    settings["refresh_token"] = refresh_token
    settings["retrieved_token"] = True

    InteractJSON.writeToFile(settings)

    print("\nYou are authenticated with Dropbox.  Please run 'python [or python3] dbx.py' again!")
except Exception as e:
    settings["retrieved_token"] = False
    InteractJSON.writeToFile(settings)
    
    print('Error: %s' % (e,))
    exit(1)
