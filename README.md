# Overview 

When ran, this script will go back one directory and check if there is a directory called ```world-backup```.  
- If there is no such directory, the script will copy the contents of the ```world``` directory and paste them into a new directory called ```world-backup```.  

- If there is such a directory, the script will "override" the ```world-backup``` directory with the content found in the ```world``` directory.

Note: this script *does not* copy every file of your Minecraft server, *only* your world files!

It is currently an idea for this script to connect with your Google Drive (and possibly Dropbox) account so you can store a copy of your backup somewhere else besides your computer.

# Insturctions on How to Use

To use this script, ensure that you have Python 3.10 (or later) installed.  Next locate the folder for your Minecraft Server.  The contents of this folder should look similar to the image below:

<div align="center">
    <img src="images/server-files.png" width="500px">
</div>

Next, create a folder named ```'script'```, with it placed in the root directory of your Minecraft server. Next, copy ```main.py``` and ```LICENSE.md``` into that folder.  It is important that you copy ```main.py``` into that folder or the script will not work!  The ```LICENSE.md``` is simply in the ```script``` directory to comply with the terms found in the [license](LICENSE.md) of this project.  Next, open up a terminal, cd to the ```script``` directory, and run ```python main.py```.

# Compatibility

This script works for the following operating system(s):

<img src="https://upload.wikimedia.org/wikipedia/commons/b/b6/Cropped-Windows10-icon.png" width=75px>
&nbsp;&nbsp;
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Apple_logo_grey.svg/1280px-Apple_logo_grey.svg.png" width=60px>
&nbsp;&nbsp;
<img src="https://upload.wikimedia.org/wikipedia/commons/f/f1/Icons8_flat_linux.svg" height=85px>

# Modules Used 

Built-in Python Libraries:

- ```shutil```: used to copy and remove specified directories
- ```os```: used to find a specified directory
- ```time```: suspend script execution

# License

This project uses the MIT license. Please ensure you retain the license notice if you use any part of my program. For more information about the licensing of this project, please see [LICENSE.md](LICENSE.md).