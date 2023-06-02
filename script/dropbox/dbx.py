#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

# my own module that interacts with the Dropbox API
from dbx_classes import DropboxApp

# authenticate using a function defined in a class in 'dbx_classes.py' which calls 'dbx-auth.py'
DropboxApp.dbxAuthenticate()

# check if there is a 'world-backup' folder in Dropbox; returns True or False
worldBackup = DropboxApp.checkForFolder("world-backup")

# create a world-backup folder IF it does not exist in Dropbox
if (worldBackup == False):
    # ask to create a 'world-backup' folder
    askToCreate = input("\nDo you wish to create a backup folder [y/n]: ")
    askToCreate.lower
    print("\n")

    if askToCreate == "y" or askToCreate == "yes":
        DropboxApp.createFolder("world-backup", True)
    else:
        print("If you want to create a folder, run \"python [or python3] dbx.py\"!\n")
elif(worldBackup == True):
    # ask to upload the  'world-backup' folder
    askToUpload = input("\nDo you wish to backup your folder to Dropbox [y/n]: ")
    askToUpload.lower
    print("\n")

    # upload the contents of 'world-backup' from the user's computer to dropbox in the "newly" created folder
    if askToUpload == "y" or askToUpload == "yes":
        DropboxApp.uploadFolder("world-backup", "world-backup")
    else:
        print("If you want to backup your folder, run \"python [or python3] dbx.py\"!\n")



