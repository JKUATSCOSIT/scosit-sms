
from __future__ import print_function
import httplib2
import os
import logging

import sqlite3
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from tasks import send_message
from config import Config

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-scosit-sms.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_email_and_phone():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/{spread sheet id}/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '{spreadsheetid}'.format(
        spreadsheetid=Config.SHEET_ID)
    rangeName = Config.QUERY
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()

    values = result.get('values', [])

    if not values:
        yield "No Values found"
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            phone_number = row[2]
            try:
                assert(phone_number.startswith("+"))
            except Exception as e:
                phone_number = "+254" + phone_number[:9]
            yield row[0], phone_number



def main():
    """Creates a db instance and saves data to disk
    """
    count = 0
    for name, phone_number in get_email_and_phone():
        count += 1
        print("Sending message to {name}".format(name=name))
        send_message.apply_async(args=[dict(name=name,phone_number=phone_number)])
    print("Done. Sent {count} Messages".format(count))

if __name__ == '__main__':
    main()