##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

from ._version import __version__

import requests

dev_version = 'dev' in __version__.lower()

session = None

def get_session():
    global session
    if session is None:
        session = requests.session()
        if dev_version: print('Creating session')
        return session
    else:
        if dev_version: print('Re-using session')
        return session
