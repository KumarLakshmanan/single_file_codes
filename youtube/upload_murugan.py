#!/usr/bin/python
import os
import sys
import json
import time
import random
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

API_NAME = 'youtube'
API_VERSION = 'v3'
MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_FILE = './client_secret.json'
TOKEN_FILES = [
    "./tokens/murugan-tamilkadavul.json",
]

# Set the OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly',
          'https://www.googleapis.com/auth/youtube',
          'https://www.googleapis.com/auth/youtube.force-ssl',
          'https://www.googleapis.com/auth/youtubepartner',
          'https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service(token_file):
    try:
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        return build(API_NAME, API_VERSION, credentials=creds)
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def resumable_upload(insert_request):
    retry = 0
    while True:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response and 'id' in response:
                print(f"Video uploaded successfully: {response['id']}")
                return response
            else:
                print(f"Unexpected response: {response}")
        except HttpError as e:
            print(f"HTTP error: {e}")
            print(f"HTTP error: {e.resp.status}")
            print(f"HTTP error: {e.resp.reason}")
            if e.resp.status in RETRIABLE_STATUS_CODES:
                print(f"Retrying due to HTTP error: {e.resp.status}")
            else:
                print(f"HTTP error: {e.resp.status}")
                return None
        retry += 1
        if retry > MAX_RETRIES:
            print("Upload failed after multiple retries.")
            return None
        sleep_seconds = random.uniform(1, 2 ** retry)
        print(f"Retrying in {sleep_seconds:.2f} seconds...")
        time.sleep(sleep_seconds)

def upload_video(service, video_file, name):
    body = {
        "status": {
            "privacyStatus": "private",
            "madeForKids": False
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = service.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    resumable_upload(request)

def main():
    video_path = "./murugan_output/NOT UPLOADED/"
    video_files = [f for f in os.listdir(video_path) if f.endswith(".mp4")]
    os.makedirs("./murugan_output/UPLOADED/", exist_ok=True)

    fileCount = 0
    for token in TOKEN_FILES:
        for thisTokenCount in range(10):
            if (fileCount >= len(video_files)):
                break

            video_file = video_path + video_files[fileCount]
            print(f"Token: {token}")
            service = get_authenticated_service(token)
            if not service:
                continue
            try:
                channels_response = service.channels().list(part='snippet', mine=True).execute()
                channels = channels_response.get('items', [])
                if not channels:
                    print("No channels found.")
                    continue

                for channel in channels:
                    uploadYes = input("Do you want to upload this video " + channel['snippet']['title'] + " YT Channel ? (y/n): ")
                    if uploadYes.lower() == 'y':
                        print(f"File: {video_file}")
                        print(f"Uploading video to channel: {channel['snippet']['title']}")
                        fileName = video_files[fileCount].split("____")[0]
                        upload_video(service, video_file, fileName)
                        os.rename(video_file, f"./murugan_output/UPLOADED/{video_files[fileCount]}")
                        fileCount += 1
            except Exception as e:
                print(f"API error: {e}")

if __name__ == '__main__':
    main()
