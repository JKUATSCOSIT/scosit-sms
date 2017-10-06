
from __future__ import print_function
import httplib2
import os
import logging

import sqlite3
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

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
                                   'sheets.googleapis.com-python-quickstart.json')

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

    spreadsheetId = 'spreadsheet id'
    rangeName = 'form query'
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


def gateway():
    AT_APIKEY = "your api key"
    AT_USERNAME = "you username"
    environment = None    # change this to 1 for testing
    if environment is None:
        gateway = AfricasTalkingGateway(apiKey=AT_APIKEY, username=AT_USERNAME)
    else:
        gateway = AfricasTalkingGateway(apiKey=AT_APIKEY, username="sandbox", environment="sandbox")
    return gateway


def main():
    """Creates a db instance and saves data to disk
    """
    # create an in memory db connection instance
    # conn = sqlite3.connect(':memory:')
    # c = conn.cursor()

    # create a db table
    # print("Creating table")
    # try:
    #     c.execute('''CREATE TABLE   users(name text, phone_number text)''')
    #     print("Table created")
    # except Exception as exc:
    #     pass

    print("Getting values from spreadsheet")
    sms_gateway = gateway()
    message = "Dear {name}" \
              "\nThank you for expressing interest in attending today's SCOSIT meeting hosted by BRAVE ventures\n" \
              "Please come with your laptop and be seated by 7:00PM.\n" \
              "The venue for the meeting is HALL 7 ROOM 32\n" \
              "Kind regards,\n" \
              "Pius Dan - SCOSIT"
    for name, phone_number in get_email_and_phone():
        try:
            print("sending sms to {name}".format(name=name))
            sms_gateway.sendMessage(to_=[phone_number], message_=message.format(name=name))
            print ("message sent")
        except AfricasTalkingGatewayException as exc:
            print ("Failed to send an sms to {name} with error {error}".format(name=name, error=exc.__str__()))

    #     c.execute('INSERT INTO users VALUES (?,?)', [name, phone_number])
    # print("Storing to db")
    # conn.commit()
    # print("Values stored")


    # print("closing db connection")
    # conn.close()
    # print("connection closed")

if __name__ == '__main__':
    main()
