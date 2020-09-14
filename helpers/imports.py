"""
This module includes library functions that are useful for other scripts.
"""

import pickle
import os.path
import re

import gspread
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# scopes for data access: https://developers.google.com/drive/api/v3/about-auth
# if you modify these, delete token.pickle
SCOPES = ['https://www.googleapis.com/auth/drive'
          'https://www.googleapis.com/auth/drive.appdata']


def auth_gdrive():
    """
    Authenticates client to use the Google Drive v3 API.

    :return: Service object with authentication for Google Drive v3 API.
    """
    # store credentials
    creds = None

    # the file token.pickle stores the user's access and refresh tokens, and is created automatically when the
    # authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # if there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # auth user and return the authentication service for other functions
    return build('drive', 'v3', credentials=creds)


def auth_gsheets():
    """
    Authenticates client to read and write data to Google Spreadsheets.

    :return: gspread authentication object.
    """
    return gspread.service_account("service_account.json")

def get_file_id_from_url(file_url):
    """
    Retrieves a Google Drive file id from a given Google Drive file url.

    :param file_url: string url for a Google Drive file.
    :return: string file id parsed from file url.
    :raises exception: exception if not given a file url
    """
    # attempt to match a document by checking if /d/ is found
    results = re.search(r"/d/(.+)/", file_url)

    if results:
        return results.group()[3:-1]

    # raise exception if not found
    raise Exception("Invalid Google Drive file URL: expected '/d/' was not found.")


def get_folder_id_from_url(folder_url):
    """
    Retrieves a Google Drive folder id from a given Google Drive folder url.

    :param folder_url: string url for a Google Drive folder.
    :return: string folder id parsed from folder url.
    """
    # attempt to match a document by checking if /d/ is found
    results = re.search(r"/folders/(.+)", folder_url)

    if results:
        return results.group()[9:]

    # raise exception if not found
    raise Exception("Invalid Google Drive folder URL: expected '/folders/' was not found.")
