#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

import os
import json
import dropbox
from decouple import config 
import subprocess
import re

class InteractJSON:
    # when called, if a 'dbx-credentials.json' file is not present, then one will be created, 
    # with object(s) passed in as a parameter (named data)
    def createFile(data):
        filename = "dbx-credentials.json"
        isFile = os.path.isfile(filename)

        if(not isFile):
            with open(filename, 'w') as f:
                json.dump(data, f, indent = 4)
            print("\nA 'dbx-credentials.json' file has been created. By default, there will be no credentials stored. "
            + "Running 'dbx.py' or 'dbx-auth.py' will auto-populate the necessary data.\n")

    # read 'dbx-credentials.json'
    def readFile():
        try:
            with open('dbx-credentials.json', 'r') as f:
                settings = json.load(f)
            f.close()

            return settings
        except:
            data = {
                "retrieved_token": False,
                "generated_access_code": None,
                "access_token": None,
                "refresh_token": None
            }

        InteractJSON.createFile(data)

        with open('dbx-credentials.json', 'r') as f:
            settings = json.load(f)
        f.close()

        return settings

    # write/override object data in 'dbx-credentials.json'
    def writeToFile(settings):
        with open('dbx-credentials.json', 'w') as f:
            json.dump(settings, f, indent = 4)
        f.close()

APP_KEY = config("APP_KEY")
auth = InteractJSON.readFile()

class DropboxApp:
    def dbxAuthenticate():
        """
        Authenticate with the Dropbox API.  dbxAuthenticate() requires a 'dbx-credentials.json' file to be present.
        The user does not need to make one IF THERE IS NOT ONE PRESENT!  dbxAuthenticate() will handle that by using
        the 'InteractJSON' class in 'dbx_classes.py'
        """

        data = {
            "retrieved_token": False,
            "generated_access_code": None,
            "access_token": None,
            "refresh_token": None
        }

        InteractJSON.createFile(data)

        settings = InteractJSON.readFile()

        # to make things more convenient, 'dbx-auth.py' will automatically run 
        # to retrieve access and refresh tokens, as well as generating an access code 
        # and storing them in 'dbx-credentials.json'
        if (settings['retrieved_token'] == False):
            subprocess.call(['python3', 'dbx-auth.py'])
        else:
            print("You are already authenticated with the Dropbox API.  If you want to refresh any token, run 'dbx-auth.py'.\n")

    def createFolder(folderName, printMessage):
        """
        folderName: will create a folder in your Dropbox based upon what string you pass in.
        Ensure that you do not include any characters (besdies letters) when passing in this parameter.
        
        If you want to pass in an integer, put it in between double quotes (e.g. "1").
        If an integer or boolean is passed as a parameter, DropboxApp.createFoler will raise a TypeError 
        and terminate the execution of the function.

        printMessage: either True or False.  If true, then a message will be printed to the console saying 
        either creating the folder was a success or it failed.  If false, will not print any message to console.
        """

        # prevent from passing in a boolean as a parameter
        if(type(folderName) == bool or type(folderName) == int):
            raise TypeError("Ensure you pass in a string, not an integer or boolean.")

        # authenticate with Dropbox
        global APP_KEY 
        global auth

        try:
            dbx = dropbox.Dropbox(
                app_key=APP_KEY,
                oauth2_refresh_token=auth['refresh_token']
            )
        except:
            settings = InteractJSON.readFile()
            if (settings["retrieved_token"] == False):
                print("DropboxApp.createFolder(): There was an error.  Make sure you are authenticated with Dropbox.")

        # create the folder; the try except statement is here because if one parameter in 'files_create_folder_v2' 
        # is False and Dropbox sees there is already a folder named 'folderName', then it will throw an error
        # I do not want to set 'files_create_folder_v2' to True to create duplicate, renamed folders
        try:
            dbx.files_create_folder_v2("/" + str(folderName), False)
            if printMessage == True:
                print("DropboxApp.createFolder: " + str(folderName) + " has been successfully created!\n")
        except:
            pass
        
    def checkForFolder(folderName):
        """
        folderName: this will tell Dropbox what folder to be looking for.  For example, pass in "world-backup" and 
        the function will call the Dropbox API to check the users Dropbox for that folder name.  Returns a boolean.

        If you want to pass in an integer, put it in between double quotes (e.g. "1").
        If an integer or boolean is passed as a parameter, DropboxApp.createFoler will raise a TypeError 
        and terminate the execution of the function.
        """

        # prevent from passing in a boolean as a parameter
        if(type(folderName) == bool or type(folderName) == int):
            raise TypeError("Ensure you pass in a string, not an integer or boolean.")

        # authenticate with Dropbox
        global APP_KEY 
        global auth

        try:
            dbx = dropbox.Dropbox(
                app_key=APP_KEY,
                oauth2_refresh_token=auth['refresh_token']
            )
        except:
            settings = InteractJSON.readFile()
            if settings["retrieved_token"] == False:
                print("DropboxApp.createFolder(): There was an error.  Make sure you are authenticated with Dropbox.")

        # check for folder
        try:
            dbx.files_list_folder("/" + folderName)

            print("DropboxApp.checkForFolder: A folder named '" + folderName + "' was found in your Dropbox.")

            return True
        except:
            print("DropboxApp.checkForFolder: A folder named '" + folderName + "' was not found in your Dropbox...")

            return False

    def uploadFolder(localFolder, dropboxFolder):
        """
        localFolder: get the name of the local folder to upload to Dropbox.  
        Ensure that you do not include any characters (besdies letters) when passing in this parameter.

        dropboxFolder: destination of the folder in Dropbox
        
        If you want to pass in an "integer", put it in between double quotes (e.g. "1") so it is a string.
        If an integer or boolean is passed as a parameter, DropboxApp.uploadFolder will raise a TypeError 
        and terminate the execution of the function. 
        """

        # prevent from passing in a boolean as a parameter
        if(type(localFolder) == bool or type(localFolder) == int):
            raise TypeError("Ensure you pass in a string, not an integer or boolean.")

        # authenticate with Dropbox
        global APP_KEY 
        global auth

        try:
            dbx = dropbox.Dropbox(
                app_key=APP_KEY,
                oauth2_refresh_token=auth['refresh_token']
            )
        except:
            print("DropboxApp.createFile(): There was an error.  Make sure you are authenticated with Dropbox.")

        # main part of the function

        # declare all needed variables
        rootOfBackup = os.path.abspath("../../" + localFolder)

        filesInRoot = []
        dirsInRoot = []
        
        ### ======= ### ======= ###     

        # ROOT DIR
        for filename in os.listdir(rootOfBackup):
            f = os.path.join(rootOfBackup, filename)

            if os.path.isfile(f):
                filesInRoot.append(f)

        # remove .DS_STORE

        indexOfDS_Store = filesInRoot.index(rootOfBackup + "/.DS_Store")
        filesInRoot.pop(indexOfDS_Store)

        # UPLOAD ROOT DIR FILES

        filesInRootCounter = 0
        uploadCounter = 0

        for i in filesInRoot:
            dbxFile = (re.split("/", " ".join([i])))

            with open(" ".join([i]), 'rb') as f:
                dbx.files_upload(f.read(), "/" + dropboxFolder + "/" + dbxFile[-1])
                print("Uploading: " + dbxFile[-1])
                
                filesInRootCounter += 1
                uploadCounter += 1
            
        print("\nFinished uploading files in root directory.  Uploaded " + str(filesInRootCounter) + " file(s).\n")
        
        ### ======= ### ======= ###

        # SUBDIRS IN ROOT DIR

        for dirs in os.listdir(rootOfBackup):
            f = os.path.join(rootOfBackup, dirs)

            if os.path.isdir(f):
                dirsInRoot.append(f)

        dirsInRootCounter = 0

        for i in dirsInRoot:
            dbxDir = (re.split("/", " ".join([i])))
            DropboxApp.createFolder(dropboxFolder + "/" + dbxDir[-1], False)
            print("Uploading: '" + dbxDir[-1] + "' directory")

            dirsInRootCounter += 1
            uploadCounter += 1

        print("\nFinished creating folders in root directory.  Uploaded " + str(dirsInRootCounter) + " folder(s).\n")
        
        # TODO UPLOAD ALL FILES FROM SUBFOLDERS OF ROOT DIR TO DROPBOX
        
        # print("Starting to upload the folders files...")
        print("\n\nUploaded a total of " + str(uploadCounter) + " file(s) and/or folder(s) to Dropbox\n")
        
        # because the upload function is incompelte, I will simply raise an error
        raise UserWarning("DropboxApp.uploadFolder: function incomplete; still need to upload files to subdirectories!")
        
        # end of function