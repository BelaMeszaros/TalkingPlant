#!/usr/bin/env python3#-------------------------------------------------------------------------------
# Name:        Talking plant - upload
# Purpose:     Syncronise files on an ftp server directory with files in the
#              working directory. Only the files specified with a regexp will
#              be syncronised.
#              dir.txt will contain the md5 hash of the files to be syncronised
#              one file per line.
#
# Author:      MeszarB[]
#
# Created:     09/08/2014
# Copyright:   (c) MeszarB 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

FTP_SERVER = "surplus.x10.bz"
FTP_FOLDER = "/public_html/TalkingPlant/"
FTP_USER = "scriba"
FTP_PSW = "So1d3us"
FTP_FILES = "\.png$"

from ftplib import FTP
import sys
import os
import re
import hashlib

def dirLocal():
    fileFilter = re.compile(FTP_FILES)
    curDir = os.listdir('.')
    return [hashlib.md5(open(f,'rb').read()).hexdigest() + " " + f for f in curDir if fileFilter.search(f) != None]

def main():
    # prepare the files to upload
    fileList = dirLocal() # files and md5s in the local directory
    # ask for confirmation
    print ("You will upload the following "+str(len(fileList))+" file(s) to the server folder.")
    print ("All other files will be deleted from the server folder!")
    for fn in fileList:
        print(fn[33:])
    resp ="0"
    while not(resp in ['y', 'Y', 'n', 'N', '']):
        resp = input("Do you want to continue? (y/N)")
        if resp == 'n' or resp == 'N' or resp == '':
            return("Aborted by user")
    # prepare dir.txt
    f = open("dir.txt", mode="w")
    for fn in fileList:
        print(fn, file=f)
    f.close()
    # creating connection to server and set wd
    print("Connecting...")
    try:
        ftp = FTP(FTP_SERVER, FTP_USER, FTP_PSW)
        ftp.cwd(FTP_FOLDER)
    except:
        return ("Unexpected error at login:", sys.exc_info()[0])
    # delete all file from server folder
    print("Deleting old files")
    try:
        serverList = ftp.nlst()
        for fn in serverList:
            if fn != "." and fn != "..":
                ftp.delete(fn)
    except:
        return ("Unexpected error at deleting old files:", sys.exc_info()[0])
    print("Uploading files")
    try:
        for fn in fileList:
            f = open(fn[33:], "rb")
            print(fn[33:] + ":")
            print(ftp.storbinary("STOR "+fn[33:], f))
            f.close()
        f = open("dir.txt", "rb")
        ftp.storbinary("STOR dir.txt", f)
        f.close()
    except:
        return ("Unexpected error at uploading:", sys.exc_info()[0])
    try:
        ftp.quit()
    except:
        return ("Unexpected error at quit:", sys.exc_info()[0])
    return ("Everything went OK")

if __name__ == '__main__':
    print(main())
