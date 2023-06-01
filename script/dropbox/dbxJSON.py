#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

import os
import json

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
        with open('dbx-credentials.json', 'r') as f:
            settings = json.load(f)
        f.close()

        return settings

    # write/override object data in 'dbx-credentials.json'
    def writeToFile(settings):
        with open('dbx-credentials.json', 'w') as f:
            json.dump(settings, f, indent = 4)
        f.close()