<span>
    <a href="https://github.com/dropbox/dropbox-sdk-python" target="_blank">
        <img src="https://img.shields.io/badge/Dropbox%20API-v11.36.1-blue.svg?style=for-the-badge&logo=Dropbox&style=plastic"></img>
    </a>
</span>
<span>
    <a href="https://github.com/googleapis/google-api-python-client" target="_blank">
        <img src="https://img.shields.io/badge/Google%20API-v2.88.0-blue.svg?style=for-the-badge&logo=GoogleDrive&style=plastic"></img>
    </a>
</span>
<span>
    <img src="https://img.shields.io/badge/project%20status-in%20active%20development-brightgreen"></img>
</span>


# Overview 

When ran, this script will go back one directory and check if there is a directory called ```world-backup```.  
- If there is no such directory, the script will copy the contents of the ```world``` directory and paste them into a new directory called ```world-backup```.  

- If there is such a directory, the script will "override" the ```world-backup``` directory with the content found in the ```world``` directory.  If for some reason your world is gone and you have a backup, all you need to do is rename ```world-backup``` to ```world``` and place it in the root directory of your Minecraft Server

Note: this script *does not* copy every file of your Minecraft server, *only* your world files!

This script can also upload your ```world-backup``` to the following cloud services:

- Dropbox
    - Drobox is fully implemented.  If you want to use Dropbox, scroll down to [#Dropbox](#dropbox) in this README file.

- Google Drive
    - I am currently working on uploading ```world-backup``` to Google Drive.

# Insturctions on How to Use

To use this script, ensure that you have Python 3.10 (or later) installed.  Next locate the folder for your Minecraft Server.  The contents of this folder should look similar to the image below:

<div align="center">
    <img src="images/server-files.png" width="500px">
</div>

Next, copy the ```'script'``` directory of this project and place it in the root directory of your Minecraft server. Next, copy ```LICENSE.md``` file into that folder.  The ```LICENSE.md``` is simply in the ```script``` directory to comply with the terms found in the [license](LICENSE.md) of this project.  

If you are wanting to copy your world files,

- Open up a terminal, cd to the ```script``` directory, and run ```python main.py```.

If you are wanting to upload your world files,

- Dropbox: see [#Dropbox](#dropbox)
- Google Drive: feature in-progress; see [#Google Drive](#google-drive)

# Dropbox

There are two requirements in order to use Dropbox with this script: registering a Dropbox app and installing the proper modules.

## Registering a Dropbox App

- In order to register a Dropbox App, go to [register a Dropbox app](https://www.dropbox.com/developers/apps/create) so you can connect to the Dropbox API (ensure you select "Full Dropbox Access" when registering your app).  

    - After registering your app, go to the [App Console](https://www.dropbox.com/developers/apps), access your app, and click the tab, 'Permissions'.  Ensure you have the following checked:

        - files.metadata.write
        - files.content.write
        - file_requests.write

    - After doing that, go to the 'Settings' tab of your app.  Once there, scroll down until you find "App key".  Copy that key.  If you copied the script directory to the root of your Minecraft server, you should see a subdirectory named ```dropbox```in ```script```.  In the ```dropbox``` folder, create a file named ```.env``` and add the following text: "APP_KEY=[paste the app key you copied here]".

<div align="center">
    <img src="images/env-variables.png" width="500px">
</div>

## Installing Modules

- Ensure you have the following Python Modules installed for Dropbox to work:

    - pip install ```dropbox```
    - pip install ```python-decouple```

## Uploading to Dropbox

There is ***full*** functionality for uploading folders and files to Dropbox.  However, this script ***will not*** upload your /datapacks folder (sorry!).

In you copied the ```script``` directory to the root of your Minecraft server, you will have a subdirectory named ```dropbox``` in ```script```.  Within this directory, you should have three Python script files: ```dbx.py```, ```dbx_auth.py```, and ```dbx_classes.py```.  Additionally, you should have already added your ```.env``` file with the necessary variable(s).  **You do not need to run ```dbx_auth.py``` or ```dbx_classes.py```.**

To upload your world files to Dropbox,

- Open up a terminal, cd to the ```script/dropbox``` directory, and run ```python dbx.py```.  If you have followed the above directions, you will be asked to authenticate with the Dropbox API and will be given instructions (in the console) and be redirected to a link.

- Then, run ```python dbx.py``` again and follow the directions.

# Google Drive

There are two requirements in order to upload to Google Drive with this script: registering with the Google API and installing the proper modules.

## Registering with the Google API

Registering with the Google API is more complicated than Dropbox, but still manageable.

- Open [console.cloud.google.com/projectcreate](https://console.cloud.google.com/projectcreate) to begin creating a project.  Name the project, and if desired, edit the project ID.  Press "Create".

- You will then be redirected (note, if you have created any projects before, you may have been redirected to an older project; check that you are connected to the project you just created by going to the top left of your window click on the dropdown by the "Google Cloud" logo).  Then, scroll down until you see a section named "Getting Started" and select "Explore and enable APIs".  (This is the apis dashboard).

- On the left, there is a tab labeled "Enabled APIs & services".  Click that.  Then click "Enable APIs and Services".

- In the search bar, type "Google Drive API" and press enter

- Select "Google Drive API"

- Press the "Enable" button to enable the Google Drive API

You should then be redirected to the [APIs dashboard](https://console.cloud.google.com/apis/dashboard).  Ensure you still are in your newly created project.

- On the left, there is a tab labeled "OAuth consent screen".  Click that.  Then select "External" user type (or "Internal" if you are a Google Workspace user) and then "Create".

You should be on the following screen: "(1) OAuth consent screen"

- You are required to add the following information:

    - Enter your app name
    - Enter the user support email
    - App logo (optional)
    - App domain (optional, I used "Authorized domains" instead of "App domain")
    - Authorized domains; click "Add Domain" add type in "www.googleapis.com".  This will redirect you to Google's authentication screen
    - Enter your developer contact (email) information
    - Save and continue

You should be on the following screen: "(2) Scopes"

- To add the Drive API,

    - Click "Add or Remove Scopes"
    - In the filter, type in "Drive" and select "Google Drive API"
    - These are the necessary scopes to add to your project:
        - ".../auth/docs"
        - ".../auth/drive"
        - ".../auth/drive.metadata.readonly"
    - Then, click "Update"
    - Scroll down, and click "Save and Continue"

You should be on the following screen: "(3) Scopes"

- To add use your app, click "Add Users", enter your email, and click "Add"
- "Save and Continue"

You will be on a screen that will summarize your app registration.  Once done, scroll down and click "Back to Dashboard".

- On the left, there is a tab labeled "Credentials".  Click that.  At the top, click "Create Credentials" and then "OAuth client ID".

- For the application type, select "Dekstop app".  Name the OAuth 2.0 client, then press create.  

- Download the JSON and drag it to the ```drive``` folder in the ```script``` directory.  Rename the JSON to "drive-credentials.json".  

See [#Installing Modules](#installing-modules-1) and then [#Uploading to Google Drive](#uploading-to-google-drive) to authenticate and use the Google Drive API

## Installing Modules

- Ensure you have the following Python Modules installed for Dropbox to work:

    - pip install --upgrade ```google-api-python-client google-auth-httplib2 google-auth-oauthlib```

## Uploading to Google Drive

The feature for uploading to Google Drive is currently being developed.

Ensure you have the following files in ```script/drive```:

- ```drive_auth.py```
- ```drive_classes.py```
- ```drive.py```
- ```drive-credentials.json```, an OAuth client JSON file downloaded from [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)

Right now (with its limited features), this script can do the following:

- Authenticate with the Google Drive API and create a folder named "Test"

    - cd to ```script/drive``` and run ```python drive.py```.  You will then be asked to authenticate with the API.  When done successfully, ```drive.py``` will then create a folder named "Test"

# Compatibility

This script works for the following operating system(s):

*Note: I do not have access to a Linux system to test out these scripts.  Do not expect them to work :)

<span>
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b6/Cropped-Windows10-icon.png" width=75px>
</span>
<span>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Apple_logo_grey.svg/1280px-Apple_logo_grey.svg.png" width=60px>
</span>


# API(s) and Modules Used 

API:

- [Dropbox API](https://www.dropbox.com/developers) ([Python SDK](https://www.dropbox.com/developers/documentation/python)) ([GitHub Source Code](https://github.com/dropbox/dropbox-sdk-python))

- [Google Drive API](https://developers.google.com/drive/api/guides/about-sdk) ([Python SDK](https://developers.google.com/drive/api/guides/api-specific-auth))

Built-in Python Libraries:

- ```shutil```: used to copy and remove specified directories
- ```os```: used to find a specified directory
- ```webbrowser```: used to open URLs in your browser
- ```time```: suspend script execution
- ```re```: string comparisons
- ```json```: read and write to JSON files

Installed Modules:

- [```dropbox```](https://pypi.org/project/dropbox/): connect to and use the Dropbox API
- Google Drive:
    - ```google-api-python-client ```
    - ```google-auth-httplib2 ```
    - ```google-auth-oauthlib```
- [```python-decouple```](https://pypi.org/project/python-decouple/): open .env files and read environment varibales


# License

This project uses the MIT license. Please ensure you retain the license and copyright notices if you use any part of my program. For more information about the licensing of this project, please see [LICENSE.md](LICENSE.md).

In addition to a MIT license being used in this project (by me, Kenner Hartman), I have included code written by Google (which I have modified).  To comply with the licesnse they use (found on thier [GitHub](https://github.com/googleworkspace/python-samples/blob/main/LICENSE)), you will see an additional license named "Apache 2.0" in [LICENSE.md](LICENSE.md).  This license applies to the following file(s): 

- [```drive_auth.py```](script/drive/drive_auth.py).

Please make note of the [notice](NOTICE) included in this repository.