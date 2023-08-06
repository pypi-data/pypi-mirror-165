##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

###############################################################################################
####    File utils
####

import os, hashlib

def fix_path(path):
    return extract_drive_and_fix_path(path)[1]

# Get a windows path in a format we can use on linux
def extract_drive_and_fix_path(path):
    # Extract the drive
    drive, path = os.path.splitdrive(path)

    # Switch slashes to correct direction
    path = path.replace('\\', '/')

    return drive, path

def hash_file(fileName):
    if os.path.isfile(fileName):
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        with open(fileName, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest().upper()
    return str(None)

###############################################################################################
####    Upload progress
####

class CanceledError(Exception):
    def __init__(self, message, pathToRemove=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message
        self.pathToRemove = pathToRemove
