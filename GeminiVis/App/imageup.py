from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from googleapiclient.http import MediaFileUpload
# Replace with your credentials file path
CREDENTIALS_FILE = 'GeminiVis\App\client_secret_495548084074-feb7jjutpgse72dppj9ceogt9tpf1jl7.apps.googleusercontent.com.json'

# Define the Drive API service name and version
SCOPES = ['https://www.googleapis.com/auth/drive']


def get_authenticated_service():
  """
  Authenticates the user and builds the Drive API service.

  Returns:
      The authenticated Drive API service object.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, 
  # and is created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.json'):
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_token_file('token.json', SCOPES)
  # If there are no valid credentials available, then start the authorization flow.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          CREDENTIALS_FILE, SCOPES)
      creds = flow.run_local_server(port=0)
  # Build the Drive service object
  service = build('drive', 'v3', credentials=creds)
  return service

def upload_image_to_drive(file_path, folder_id):
  """
  Uploads an image to a specific folder in Google Drive.

  Args:
      file_path: Path to the image file.
      folder_id: ID of the target folder in Drive.

  Returns:
      The uploaded file's metadata if successful, None otherwise.
  """
  service = get_authenticated_service()
  mime_type = 'image/jpeg'  # Adjust based on image type

  file_metadata = {
      'name': os.path.basename(file_path),
      'parents': [folder_id]
  }
  try:
    media_body = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(
        body=file_metadata, media_body=media_body).execute()
    return file
  except HttpError as error:
    print(f'An error occurred: {error}')
    return None 