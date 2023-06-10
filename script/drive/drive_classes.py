#
# Copyright (c) 2023 by Kenner Hartman. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for details.
#

from drive_auth import requestCreds

class DriveApp:
    
    # sure, this function is barebones when used in 'drive.py', but I want less clutter when importing 
    # 'requestCreds' in 'drive_auth.py'
    def returnCreds():
        creds = requestCreds()
        return creds