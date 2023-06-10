#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

import os
import json
import dropbox
from decouple import config 
import re
import platform

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

# global variables for the following class and subclass
APP_KEY = config("APP_KEY")
auth = InteractJSON.readFile()
uploadCounter = 0

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
            from dbx_auth import authenticate

            # instead of using subprocess.call() to run 'dbx_auth.py', directly call the 
            # authenticate function in 'dbx_auth.py' to authenticate with Dropbox
            authenticate()
            
            # why is this exit(0) function declared here?  when delcaring DropboxApp.dbxAuthenticate and then declaring 
            # DropboxApp.checkFolder in 'dbx.py', the script will, for some reason, not recognize there is a
            # folder named 'world-backup' and will throw an exception that the folder does not exsist 
            # (EVEN THOUGH IT DOES!). I do not find terminating the script entirely to be a big deal since
            # you really only need to authenticate with Dropbox once.
            exit(0)
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

    # this subclass will deal with uploading the files to Dropbox

    # DropboxApp.Upload.getDirectories() should only be called by other functions in this subclass,
    # and not be referenced in any other file

    class Upload:
        def getDirectories(folderPath):
            """
            folderPath: the target folder on the user's local machine to upload to Dropbox

            This function should not be called outside of 'dbx_classes.py' as it serves no purpose
            other than to return the root directory, root files, and sub directories in the root directory 
            of the folderPath.
            """
            rootDir = []
            rootFiles = []
            subDir = []

            rootOfBackup = os.path.abspath("../../" + folderPath)

            for dir in os.listdir(rootOfBackup):
                fDirs = os.path.join(rootOfBackup, dir)

                if os.path.isdir(fDirs):
                    rootDir.append(fDirs)

            for filename in os.listdir(rootOfBackup):
                files = os.path.join(rootOfBackup, filename)

                if os.path.isfile(files):
                    rootFiles.append(files)

            for i in range(len(rootDir)):
                for dir in os.listdir(os.path.join(rootOfBackup, rootDir[i])):
                    fDirs = os.path.join(rootDir[i], dir)

                    if os.path.isdir(fDirs):
                        subDir.append(fDirs)

            return rootDir, rootFiles, subDir

        def overwriteFolder(folderPath):
            """
            folderPath: the target Dropbox folder to "overwrite" (delete)
            """

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
            
            try:
                print("Overwriting \"" + folderPath + "\" folder...\n")
                dbx.files_delete_v2("/" + str(folderPath))
            except:
                pass
        
        def uploadFiles(folderPath):
            """
            folderPath: the target Dropbox folder to upload files to

            DropboxApp.Upload.uploadFiles() depends on DropboxApp.Upload.getDirectories().  The purpose of 
            this function is to upload *most* files and folders found in the 'world-backup' folder.  The only
            folder that will NOT be uploaded to Dropbox is 'datapacks'.

            There are three sections to this function: uploading to root directory; uploading directories found in the 
            root directory and all of its files; uploading any sub-directories found in any directories and all of its files
            """
            # authenticate with Dropbox
            global APP_KEY 
            global auth
            global uploadCounter

            try:
                dbx = dropbox.Dropbox(
                    app_key=APP_KEY,
                    oauth2_refresh_token=auth['refresh_token']
                )
            except:
                settings = InteractJSON.readFile()
                if (settings["retrieved_token"] == False):
                    print("DropboxApp.createFolder(): There was an error.  Make sure you are authenticated with Dropbox.")
            
            rootDirs, rootFiles, subDirs = DropboxApp.Upload.getDirectories(folderPath)

            # * === Upload Files in Root Directory === * #

            print("Beginning to upload files to Dropbox... \n")

            rootFileList = []
            for i in range(len(rootFiles)):
                if platform.system() == "Windows":
                    rootFileList.append(rootFiles[i].split("\\"))
                else:
                    rootFileList.append(rootFiles[i].split("/"))

            fileAndPath = []
            for i in range(len(rootFileList)):
                fileAndPath.append("/".join([rootFileList[i][-2], rootFileList[i][-1]]))

            root = os.path.abspath("../../" + folderPath)
            rootOfBackup = re.sub("world-backup", "", root)

            for i in range(len(fileAndPath)):
                with open(rootOfBackup + fileAndPath[i], 'rb') as f:
                    print("Uploading: " + str(re.sub("world-backup", "", fileAndPath[i])))
                    dbx.files_upload(f.read(), "/" + str(fileAndPath[i]))
                    uploadCounter += 1

            # * === Upload Files in Directories Found in Root (rootDirs) === * #

            rootDirsList = []
            for i in range(len(rootDirs)):
                if platform.system() == "Windows":
                    rootDirsList.append(rootDirs[i].split("\\"))
                else:
                    rootDirsList.append(rootDirs[i].split("/"))

            rootDirsPath = []
            for i in range(len(rootDirsList)):
                if rootDirsList[i][-1] == "datapacks":
                    print("\n!!! Notice  This script will not upload your datapacks folder due to the complex nature of uploading folders and "
                    "files to Dropbox !!!\n")
                else:
                    rootDirsPath.append("/".join([rootDirsList[i][-2], rootDirsList[i][-1]]))

            rootDirsFiles = []
            for i in range(len(rootDirsPath)):
                for filename in os.listdir(rootOfBackup + rootDirsPath[i]):
                    f = os.path.join(rootOfBackup + str(rootDirsPath[i]) + "/" + filename)

                    if os.path.isfile(f):
                        rootDirsFiles.append("/".join([rootDirsPath[i], filename]))

            for i in range(len(rootDirsFiles)):
                with open(rootOfBackup + rootDirsFiles[i], 'rb') as f:
                    print("Uploading: " + str(re.sub("world-backup", "", rootDirsFiles[i])))
                    dbx.files_upload(f.read(), "/" + str(rootDirsFiles[i]))
                    uploadCounter += 1
            
            # * === Upload Files in Subdirectories in Directories found in Root (subDirs) === * #

            subDirsList = []
            for i in range(len(subDirs)):
                if platform.system() == "Windows":
                    subDirsList.append(subDirs[i].split("\\"))
                else:
                    subDirsList.append(subDirs[i].split("/"))

            subDirsPath = []
            for i in range(len(subDirsList)):
                subDirsPath.append("/".join([subDirsList[i][-3], subDirsList[i][-2], subDirsList[i][-1]]))

            subDirsFiles = []
            for i in range(len(subDirsPath)):
                for filename in os.listdir(rootOfBackup + subDirsPath[i]):
                    f = os.path.join(rootOfBackup + str(subDirsPath[i]) + "/" + filename)

                    if os.path.isfile(f):
                        subDirsFiles.append("/".join([subDirsPath[i], filename]))

            for i in range(len(subDirsFiles)):
                with open(rootOfBackup + subDirsFiles[i], 'rb') as f:
                    print("Uploading: " + str(re.sub("world-backup", "", subDirsFiles[i])))
                    dbx.files_upload(f.read(), "/" + str(subDirsFiles[i]))
                    uploadCounter += 1

            print("\n Uploaded " + str(uploadCounter) + " file(s).")