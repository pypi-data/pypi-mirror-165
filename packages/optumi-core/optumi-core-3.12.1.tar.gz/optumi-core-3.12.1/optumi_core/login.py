##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

from ._version import __version__

from .logging import optumi_format_and_log
from .sessions import get_session

## Standard library imports

# Generic Operating System Services
import time, os

# Python Runtime Services
import traceback

# Concurrent execution
from threading import Lock

# Internet Protocols and Support
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from http.cookiejar import DefaultCookiePolicy, CookieJar
import requests

# Internet Data Handling
import json, base64

# Networking and Interprocess Communication
import socket, ssl

# Structured Markup Processing Tools
import html

## Other imports
# from cryptography import x509
# from cryptography.hazmat.backends import default_backend
from pathlib import Path
import pickle

dev_version = 'dev' in __version__.lower()

ses = get_session()

lock = Lock()
loginProgress = None

split_version = __version__.split('.')
jupyterlab_major = split_version[0]
optumi_major = split_version[1]
PORTAL = 'portal' + jupyterlab_major + (optumi_major if len(optumi_major) == 2 else '0' + optumi_major) + '.optumi.net'
PORTAL_PORT = 8443
PORTAL_DOMAIN_AND_PORT = PORTAL + ':' + str(PORTAL_PORT)

domain_and_port = PORTAL_DOMAIN_AND_PORT
def get_path(domain_and_port_override=None):
    # If there is no domain passed in, use the global domain
    if domain_and_port_override == None: return 'https://' + domain_and_port
    return 'https://' + domain_and_port_override

def get_login_progress():
    try:
        lock.acquire()
        return loginProgress
    except:
        pass
    finally:
        lock.release()

def set_login_progress(message):
    global loginProgress
    try:
        lock.acquire()
        loginProgress = message
    except:
        pass
    finally:
        lock.release()


def sign_agreement(timeOfSigning, hashOfSignedAgreement):
    URL = get_path() + '/exp/jupyterlab/sign-agreement'
    try:
        return ses.post(URL, data={
            'timeOfSigning': timeOfSigning,
            'hashOfSignedAgreement': hashOfSignedAgreement,
        }, timeout=120)
    except HTTPError as e:
        return e

def get_new_agreement():
    URL = get_path() + '/exp/jupyterlab/get-new-agreement'
    try:
        return ses.get(URL)
    except HTTPError as e:
        return e

def exchange_versions(version, mode='core'):
    try:
        # Load cookies from the disk
        COOKIE_FILE = os.path.expanduser('~') + '/.optumi/' + str(mode) + '_cookies.pickle'
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'rb') as f:
                ses.cookies.update(pickle.load(f))
                if dev_version: print('reading', mode, 'cookies:')
                now = time.time()
                for cookie in ses.cookies:
                    if cookie.expires != None and cookie.expires - now < 0:
                        if dev_version: print('Clearing', cookie.name, cookie.value, cookie.domain, cookie.expires)
                        ses.cookies.clear(cookie.domain)
                if dev_version:
                    for cookie in ses.cookies:
                        print(cookie.name, cookie.value, cookie.domain, cookie.expires)
    except Exception as err:
        print(err)

    URL = get_path() + '/exp/jupyterlab/exchange-versions'
    try:
        return ses.post(URL, data={
            'version': version,
        }, timeout=120)
    except HTTPError as e:
        return e

def check_login(mode='core'):
    URL = get_path() + '/exp/jupyterlab/exchange-versions'
    try:
        return not exchange_versions('0.0.0', mode).url.endswith('/login')
    except HTTPError as e:
        return False

def login_rest_server(login_domain, login_port, token, mode='core'):
    global domain_and_port
    try:
        start_time = None
        last_domain_and_port = None
        while True:
            if start_time == None:
                start_time = time.time()
            elif time.time() - start_time > 600:  # 10 minute timeout
                return -1, "Timed out"
            # If we want to move back to using a devserver certificate we need to check for devserver.optumi.com explicitly
            # Since we are bypassing the hostname check for the SSL context, we manually check it here
            # cert = ssl.get_server_certificate((DOMAIN, 8443))
            # cert = x509.load_pem_x509_certificate(cert.encode(), default_backend())
            # name = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value
            # if name != 'devserver.optumi.com':
            #     raise ssl.SSLCertVerificationError("SSL domain check failed (" + name + " is not devserver.optumi.com)")

            login_domain_and_port = login_domain + ':' + str(login_port)

            URL = get_path(login_domain_and_port) + '/login'
            errorURL = URL + '?error'

            # We only want to print to the log when we try to contact somewhere new
            if login_domain_and_port != last_domain_and_port: 
                if dev_version: 
                    print(optumi_format_and_log(None, 'Contacting ' + URL))
                else:
                    optumi_format_and_log(None, 'Contacting ' + URL)
            
            # since it can take a long time to log in to actually log in to the station, set a longer timeout for that request
            timeout = 30 if login_domain_and_port == PORTAL_DOMAIN_AND_PORT or login_domain_and_port == "portal.optumi.net:" + str(PORTAL_PORT) else 120

            try:
                response = ses.post(URL, data={ 'login_type': 'oauth', "username": '', "password": token }, timeout=timeout)
            except URLError as err:
                if isinstance(err.reason, socket.timeout):
                    return -1, "Timed out"
                if isinstance(err.reason, socket.gaierror):
                    if login_domain_and_port == PORTAL_DOMAIN_AND_PORT or login_domain_and_port == "portal.optumi.net:" + str(PORTAL_PORT):
                        # If we failed trying to access portalAB.optumi.net or portal.optumi.net, redirect to the top level portal.optumi.net
                        login_domain = "portal.optumi.net"
                        login_port = PORTAL_PORT
                        last_domain_and_port = login_domain_and_port
                        continue
                    else:
                        # If we were trying to access a station, redirect to portalAB.optumi.net
                        login_domain = PORTAL
                        login_port = PORTAL_PORT
                        last_domain_and_port = login_domain_and_port
                        continue
                if (isinstance(err.reason, ConnectionRefusedError)):
                    time.sleep(2)
                    login_domain = login_domain
                    login_port = login_port
                    last_domain_and_port = login_domain_and_port
                    continue
                raise err

            if response.url == errorURL:
                # Parse the error message to pass on to the user
                raw_html = response.text
                try:
                    message = raw_html.split('<div class="alert alert-danger" role="alert">')[1].split('</div>')[0]
                except:
                    message = "Invalid username/password"

                if message.startswith('Redirect to: '):
                    raw  = message.replace('Redirect to: ', '', 1)
                    redirect = json.loads(html.unescape(raw))
                    if redirect['dnsName'] == 'unknown':
                        set_login_progress('Allocating...')
                        time.sleep(2)
                        login_domain = login_domain
                        login_port = login_port
                        last_domain_and_port = login_domain_and_port
                        continue
                    elif redirect['dnsName'] == 'no more stations' or redirect['dnsName'] == 'no more trial stations':
                        return -1, redirect['dnsName']
                    else:
                        set_login_progress('Restoring context...')
                        login_domain = redirect['dnsName']
                        login_port = redirect['port']
                        last_domain_and_port = login_domain_and_port
                        continue
                return -1, message

            # Save cookies to the disk
            try:
                # Load cookies from the disk
                COOKIE_FILE = os.path.expanduser('~') + '/.optumi/' + str(mode) + '_cookies.pickle'

                with open(COOKIE_FILE, 'wb') as f:
                    if dev_version:
                        print('writing', mode, 'cookies:')
                        for cookie in ses.cookies:
                            print(cookie.name, cookie.value, cookie.domain, cookie.expires)
                    pickle.dump(ses.cookies, f)
            except Exception as err:
                print(err)

            # On success return the status value 1 and the domain that we logged in to
            domain_and_port = login_domain_and_port
            return 1, login_domain_and_port
    except Exception as err:
        print(optumi_format_and_log(None, str(err)))
        traceback.print_exc()
        return -2, ""

def logout():
    URL = get_path() + '/logout'
    try:
        return ses.get(URL, timeout=120)
    except HTTPError as e:
        return e
