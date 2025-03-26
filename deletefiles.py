import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


folder_id = '1uoXnNThQwdB-C6IeKV7NKm-kX-22B8t0' 

# Authenticate Google Drive service
def authenticate_drive():
    # Path to your service account JSON key
    SERVICE_ACCOUNT_FILE = "./credentials.json"

    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate using service account
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    return build('drive', 'v3', credentials=creds)

# Function to delete a file by ID
def delete_file(file_id, drive_service):
    try:
        drive_service.files().delete(fileId=file_id).execute()
        print(f"File with ID: {file_id} has been deleted.")
    except HttpError as error:
        print(f"An error occurred: {error}")

# Function to delete all files starting with "generated_"
def delete_generated_files(drive_service):
    query = f"'{folder_id}' in parents and name contains 'generated_'"    
    try:
        # List files starting with 'generated_'
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if not files:
            print("No files found starting with 'generated_'.")
        else:
            for file in files:
                print(f"Found file: {file['name']} (ID: {file['id']})")
                delete_file(file['id'], drive_service)
    
    except HttpError as error:
        print(f"An error occurred: {error}")

# Authenticate and create the Drive service
drive_service = authenticate_drive()

# Call the function to delete generated files
delete_generated_files(drive_service)
