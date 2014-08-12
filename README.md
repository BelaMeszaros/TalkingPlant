TalkingPlant
============

Visualisation tools for TalkingPlant initiative

This project consists of three subproject:

upload.py
---------

Python script for uploading files from the local folder matching to a specific regular expression to an FTP site. This script will work on the computer responsible for distributing (and maybe generating) the image files.

Its parmaters are the following:

FTP_SERVER: url of the ftp site to use, e.g. "surplus.x10.bz"

FTP_FOLDER: folder on the ftp site, e.g. "/public_html/TalkingPlant/"

FTP_USER: user name fot the ftp site

FTP_PSW: password for the user

FTP_FILES: regualr expression for the file names of the file to be uploaded, e.g. "\.png$" filters the file names ending with ".png"

The script ask for confirmation before deleting every file on the ftp folder and uploading the new files.

Beside the files uploaded, it creates a dir.txt file in the ftp folder.

The structure of the dir.txt:

It is a simple text file.

Each line represents a file uploaded in the ftp server and ending with a newline ("\n") character.

The first 32 characters represent the md5 checksum of the file.

The 33rd character is a space.

The characters until the end of the line are the name of the file.

download.py
-----------

Python script for downloading files from the FTP site into a folder. It syncronise the content of the folder with the content of the ftp folder based on content of the dir.txt file stored in the ftp folder. It will delete every other file from the folder. This script will work on the computer, responsible for dislaying the images.

Its parmaters are the following:

FTP_SERVER: url of the ftp site to use, e.g. "surplus.x10.bz"

FTP_FOLDER: folder on the ftp site, e.g. "/public_html/TalkingPlant/"

FTP_USER: user name fot the ftp site

FTP_PSW: password for the user

LOCAL_FOLDER: the folder where the files are downloaded into, it must be relative to the local folder, e.g.  "down" means "./down/". If the folder doesn't exist it will be created.

setup.md
--------

This file describes how to setup a Raspberry Pi B+ in order to run as a display client.

+ Setup network (wired or wireless)
+ Setup watchdog
+ Setup the download script
+ Setup cron to start the download script regularly
+ Setup a fbi script to displaying the content of the script folder continuously
