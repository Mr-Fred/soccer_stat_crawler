from dotenv import load_dotenv
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import json

# Load environment variables from the .env file
load_dotenv()
service_account_key_file = "service_account.json"
# Access the API_KEY environment variable
API_KEY = os.getenv("DOC_API_KEY")
doc_id = os.getenv("DOC_ID")
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'


def get_creds(scopes):
    """
    :rtype: google.oauth2.credentials.Credentials
    """
    # Use the service account key file
    creds = service_account.Credentials.from_service_account_file(service_account_key_file)
    scoped_credentials = creds.with_scopes(scopes)
    return scoped_credentials


def read_player_stats(creds):
    try:
        service = build(serviceName='docs', version='v1', credentials=creds)
        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=doc_id).execute()
        doc_content = document.get('body').get('content')
        text = read_structural_elements(doc_content)
        return json.loads(text)

    except HttpError as err:
        print(err)


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.
        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.
        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
    return text


def main():
    """Uses the Docs API to print out the text of a document."""
    credentials = get_creds(SCOPES)
    json = read_player_stats(credentials)
    return json



if __name__ == '__main__':
    json = main()