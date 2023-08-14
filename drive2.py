import os.path
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes and credentials JSON file
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_JSON_FILE = 'credentials.json'
TOKEN_PICKLE_FILE = 'token.pickle'

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_JSON_FILE, SCOPES)
    
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token_file:
            credentials = pickle.load(token_file)
    else:
        credentials = flow.run_local_server()
        with open(TOKEN_PICKLE_FILE, 'wb') as token_file:
            pickle.dump(credentials, token_file)
    
    return credentials

def upload_file(drive_service, file_name):
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_name, mimetype='text/plain')
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File '{file_name}' uploaded with ID: {uploaded_file['id']}")

def main():
    credentials = authenticate()
    drive_service = build('drive', 'v3', credentials=credentials)
    
    file_name = 'text.txt'
    upload_file(drive_service, file_name)

if __name__ == '__main__':
    main()


