from apiclient import discovery, errors
import oauth2client
from oauth2client import client, tools
import os
import httplib2

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


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
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        credentials = tools.run(flow, store)

        print('Storing credentials to ' + credential_path)
    return credentials

def get_message():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    try:
        response = service.users().messages().list(userId='me',
                                                   labelIds=['INBOX']).execute()
        # print(response)

        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me',
                                                       labelIds=['INBOX'],
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        # print(messages)

        snippets = []
        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg['id']).execute()

            item = {}
            item['snippet'] = message['snippet']
            item['id'] = msg['id']
            snippets.append(item)

        return snippets

    except errors.HttpError, error:
        return None
