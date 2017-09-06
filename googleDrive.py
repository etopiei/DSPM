from __future__ import print_function
import httplib2 #use pip install
import os, io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.appfolder'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python For DSPM'


def get_credentials():
    """
    Gets valid user credentials from storage.

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
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    """

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

    """

class GoogleDrive:

    def __init__(self):
        self.credentials = get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v3', http=self.http)
        self.fileID = ""

    def setFileID(self, vaultName):
        fileName = "pw-" + vaultName + ".dspm"
        response = self.service.files().list(q="name='" + fileName  + "'", spaces='appDataFolder', fields='nextPageToken, files(id, name)', pageToken=None).execute()
        for file in response.get('files', []):
            self.fileID = file.get('id')

    def getPasswordFileFromDrive(self, vaultName):
        request = self.service.files().get_media(fileId=self.fileID)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(int(status.progress()*100))     

        myFile = open("pw-" + vaultName + ".dspm", "wb")
        myFile.write(fh.getvalue())
        myFile.close() 

    def addPasswordFileToDrive(self, vaultName):
        file_metadata = {
            'name': 'pw-' + vaultName + '.dspm',
            'parents': [ 'appDataFolder' ]     
        }

        media = MediaFileUpload('pw-' + vaultName + '.dspm',
                                mimetype = 'text/plain',
                                resumable = True)
                                
        myFile = self.service.files().create(body=file_metadata,
                                        media_body = media,
                                        fields='id').execute()
        self.fileID = myFile.get('id')
        print("File uploaded succesfully.")

    def syncWithDrive(self, vaultName):
        print("This will sync with drive.")
    