from read_ytube_data import get_creds
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

script_doc = '1_Zw-8-0ownce7YGhTynhtCR4K7bDzTj5b_xlFOaHqg0'
SCOPES = ['https://www.googleapis.com/auth/documents']
creds = get_creds(SCOPES)

def write_script_to_doc():
    try:
        service = build(serviceName='docs', version='v1', credentials=creds)
        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=script_doc).execute()
        # doc_content = document.get('body').get('content')


    except HttpError as err:
        print(err)


write_script_to_doc()