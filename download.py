#!/usr/bin/env python3#-------------------------------------------------------------------------------
# Name:        Talking plant - download
# Purpose:     Syncronise files on an ftp server directory with files in a
#              directory.
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
LOCAL_FOLDER = "down"

from ftplib import FTP
import sys
import os
import re
import hashlib

def dirLocal():
    if not(LOCAL_FOLDER in os.listdir(".")):
        os.mkdir("./"+LOCAL_FOLDER)
    curDir = os.listdir("./"+LOCAL_FOLDER)
    fileListF = [fn for fn in curDir]
    fileListM = [hashlib.md5(open("./"+LOCAL_FOLDER+"/"+fn,"rb").read()).hexdigest() for fn in curDir]
    return fileListF, fileListM

def main():
    # checking available files
    fileListF, fileListM = dirLocal() # files and md5s in the local directory
    # create connection
    try:
        ftp = FTP(FTP_SERVER, FTP_USER, FTP_PSW)
        ftp.cwd(FTP_FOLDER)
    except:
        return ("Unexpected error at login:", sys.exc_info()[0])
    # get dir.txt
    try:
        ftp.retrbinary("RETR dir.txt", open("./dir.txt", "wb").write)
    except:
        return ("Unexpected error at downloading dir.txt:", sys.exc_info()[0])
    f = open("./dir.txt", "r")
    serverListF = [l[33:-1] for l in f]
    f.close()
    f = open("./dir.txt", "r")
    serverListM = [l[:32] for l in f]
    f.close()
    os.remove("./dir.txt") # delete ./dir.txt, we don't need anymore
    # delete files which are not in dir.txt
    toDelete = [fn for fn in fileListF if not(fn in serverListF)]
    for fn in toDelete:
        os. remove("./"+LOCAL_FOLDER+"/"+fn)
    # download files from dir.txt if: not exists
    toDownload1 = [fn for fn in serverListF if not (fn in fileListF)]
    for fn in toDownload1:
        try:
            ftp.retrbinary("RETR "+fn, open("./"+LOCAL_FOLDER+"/"+fn, "wb").write)
        except:
            return ("Unexpected error at downloading file "+fn+":", sys.exc_info()[0])
    # download files from dir.txt if: exists, but different md5
    toDownload2 = [serverListF[sni] for fni in range(len(fileListF)) for sni in range(len(serverListF)) if serverListF[sni] == fileListF[fni] and serverListM[sni] != fileListM[fni]]
    for fn in toDownload2:
        try:
            ftp.retrbinary("RETR "+fn, open("./"+LOCAL_FOLDER+"/"+fn, "wb").write)
        except:
            return ("Unexpected error at downloading file "+fn+":", sys.exc_info()[0])
    # quit
    try:
        ftp.quit()
    except:
        return ("Unexpected error at quit:", sys.exc_info()[0])
    return (None)

if __name__ == '__main__':
    ret = main()
    if ret != None:
        print(ret)
