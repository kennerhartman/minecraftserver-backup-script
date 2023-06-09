<span>
    <a href="https://github.com/dropbox/dropbox-sdk-python" target="_blank">
        <img src="https://img.shields.io/badge/Dropbox%20API-v11.36.1-blue.svg?style=for-the-badge&logo=Dropbox&style=plastic"></img>
    </a>
</span>
<span>
    <img src="https://img.shields.io/badge/project%20status-in%20active%20development-brightgreen"></img>
</span>


# Overview 

When ran, this script will go back one directory and check if there is a directory called ```world-backup```.  
- If there is no such directory, the script will copy the contents of the ```world``` directory and paste them into a new directory called ```world-backup```.  

- If there is such a directory, the script will "override" the ```world-backup``` directory with the content found in the ```world``` directory.

Note: this script *does not* copy every file of your Minecraft server, *only* your world files!

It is currently an idea for this script to connect with your Google Drive account so you can store a copy of your backup somewhere else besides your computer.  If you want to use Dropbox, scroll down to [Dropbox](#dropbox) in this README file.

# Insturctions on How to Use

To use this script, ensure that you have Python 3.10 (or later) installed.  Next locate the folder for your Minecraft Server.  The contents of this folder should look similar to the image below:

<div align="center">
    <img src="images/server-files.png" width="500px">
</div>

Next, copy the ```'script'``` directory of this project and place it in the root directory of your Minecraft server. Next, copy ```LICENSE.md``` file into that folder.  The ```LICENSE.md``` is simply in the ```script``` directory to comply with the terms found in the [license](LICENSE.md) of this project.  

If you are wanting to copy your world files,

- Open up a terminal, cd to the ```script``` directory, and run ```python main.py```.

- Currently, this script cannot upload your files to Dropbox.  However, you can authenticate with the Dropbox API (see [Dropbox](#dropbox)).

    - Note: there is ***full*** functionality for uploading files to Dropbox.  However, this script ***will not*** upload your /datapacks folder (sorry!).  ***Please also note, there are a full host of bugs present for people running this script on Windows!  This is what I am working on right now to fix!  This script works just fine on MacOS.*** 

# Dropbox

- Currently, if you [register a Dropbox app](https://www.dropbox.com/developers/apps/create), you can connect to the Dropbox API (ensure you select "Full Dropbox Access" when registering your app).  Once you register your app, go to the [App Console](https://www.dropbox.com/developers/apps).  Once there, find your app, access it, and scroll down until you find "App key".  Copy that key.  In the ```dropbox``` folder, create a file named ```.env``` and add the following text: "APP_KEY=[paste the app key you copied here]".

<div align="center">
    <img src="images/env-variables.png" width="500px">
</div>

- Ensure you have the following Python Modules installed for Dropbox to work:

    - pip install ```dropbox```
    - pip install ```python-decouple```

- In the ```script``` directory, you will have a directory named ```dropbox```.  Within this directory, you should have two Python script files: ```dbx.py``` and ```dbx-auth.py```.  You do not need to run ```dbx-auth.py```.  If you run ```dbx.py```, you will be prompted to authenticate with the Dropbox API.  If you want to refresh your tokens, then run ```dbx-auth.py```.

# Compatibility

This script works for the following operating system(s):

*Note: Python scripts in ```dropbox``` will not run properly on Windows because of issues that need to be resolved.  These issues are currently being worked on.

**Note: I do not have access to a Linux system to test out these scripts.  Do not expect them to work :)

<span>
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b6/Cropped-Windows10-icon.png" width=75px>
</span>
<span>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Apple_logo_grey.svg/1280px-Apple_logo_grey.svg.png" width=60px>
</span>


# API(s) and Modules Used 

API:

- [Dropbox API](https://www.dropbox.com/developers) ([Python SDK](https://www.dropbox.com/developers/documentation/python)) ([GitHub Source Code](https://github.com/dropbox/dropbox-sdk-python))

Built-in Python Libraries:

- ```shutil```: used to copy and remove specified directories
- ```os```: used to find a specified directory
- ```subprocess```: used to run the ```dbx-auth.py``` script if ```dbx.py``` is ran
- ```webbrowser```: used to open URLs in your browser
- ```time```: suspend script execution
- ```re```: string comparisons
- ```json```: read and write to JSON files

Installed Modules:

- [```dropbox```](https://pypi.org/project/dropbox/): connect to and use the Dropbox API
- [```python-decouple```](https://pypi.org/project/python-decouple/): open .env files and read environment varibales


# License

This project uses the MIT license. Please ensure you retain the license notice if you use any part of my program. For more information about the licensing of this project, please see [LICENSE.md](LICENSE.md).
