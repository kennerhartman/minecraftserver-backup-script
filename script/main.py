#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

import shutil as sh
import os
import time

def overrideBackup():
    time.sleep(0.5)
    override = input("\nA backup folder for the server has been detected.  Do you want to override the current backup with a new one [y/n]: ")
    override.lower()

    if(override == "y" or override == "yes"):
        # remove directory
        sh.rmtree('../world-backup')

        # making the CLI more *fancy* to make it look like the script is being productive and is hard at work
        print("\nOverriding current backup folder with a new one", end='', flush=True)
        for x in range(3):
            time.sleep(0.9)
            print(".", end='', flush=True)

        # finally copy the folder 
        sh.copytree('../world', '../world-backup')

        # make it look like the script is working hard
        time.sleep(0.5)

        # finally tell the user that a new backup folder has been created
        print("\n\nA new backup folder has been created\n")

    elif(override == "n" or override == "no"):
        pass
    else:
        print("Error: unrecognized value")

backupExists = os.path.exists('../world-backup')

if (backupExists == False):
    print("No backup folder has been detected.  Creating one...")
    sh.copytree('../world', '../world-backup')
elif(backupExists == True):
    overrideBackup()


