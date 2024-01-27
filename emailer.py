from __future__ import print_function

import os.path
from email.message import EmailMessage
import base64
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
load_dotenv()

from generate_bet_team_list import Betting

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def get_auth_token(scope=None):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file='credentials.json', scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

class Emailsender(object):

    def __init__(self):
        pass

    def email_sender(self, creds, sender, receiver, body):

        """
            Take list of top teams that have games to today and email to receiver_email
            Print the returned message  id.
            Returns: message meta data.
            :param creds, sender, receiver, team_list

          Load pre-authorized user credentials from the environment.
          TODO(developer) - See https://developers.google.com/identity
          for guides on implementing OAuth2 for the application.
        """
        try:
            # Call the Gmail API
            service = build(serviceName='gmail', version='v1', credentials=creds)
            msg = EmailMessage()

            msg.set_content(body)
            msg['To'] = receiver
            msg['From'] = sender
            msg['Subject'] = 'Top team playing today'

            #encoded message
            encoded_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()

            create_msg = {
                    'raw': encoded_msg
                }

            #pylint: disable=E1101
            send_msg = (service.users().messages().send
                        (userId='me', body=create_msg).execute())

            print(F'Message Id: {send_msg["id"]}')

        except HttpError as error:
            print(f'An error occurred {error})')
            send_msg=None
        return send_msg

if __name__ == '__main__':
    creds = get_auth_token(SCOPES)
    sender = os.getenv('sender')
    receiver = os.getenv('receiver')
    teams = Betting()
    team_list = teams.main()
    emailer = Emailsender()
    emailer.email_sender(creds, sender, receiver, ' '.join(team_list))
