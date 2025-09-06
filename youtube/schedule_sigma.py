#!/usr/bin/python
from datetime import datetime, timedelta
import moviepy.editor as mp
import os
import sys
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import httplib2
import os
import random
import sys
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from googleapiclient.http import MediaFileUpload

# Add the current directory to the Python search path
sys.path.append("./")
API_NAME = 'youtube'
API_VERSION = 'v3'
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# Set your OAuth 2.0 client ID and client
# read the file
CLIENT_FILE = './client_secret.json'
FileData = open(CLIENT_FILE, 'r').read()
CLIENT_ID = json.loads(FileData)['installed']['client_id']
CLIENT_SECRET = json.loads(FileData)['installed']['client_secret']

# Set the path to the OAuth 2.0 token file
TOKEN_FILE = './tokens/sigma.json'

# Set the OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly',
          'https://www.googleapis.com/auth/youtube',
          'https://www.googleapis.com/auth/youtube.force-ssl',
          'https://www.googleapis.com/auth/youtubepartner',
          'https://www.googleapis.com/auth/youtube.upload']


def get_authenticated_service():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials to the token file
        with open(TOKEN_FILE, 'w') as token_file:
            token_file.write(creds.to_json())

        return build(API_NAME, API_VERSION, credentials=creds)

    except FileNotFoundError as e:
        print("File not found:", e)
    except Exception as e:
        print('An error occurred:', e)
    return None


def main():
    daycount = 0
    timecount = 0
    if not os.path.exists(TOKEN_FILE):
        service = get_authenticated_service()
    else:
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        service = build(API_NAME, API_VERSION, credentials=creds)

    videos = []  # To store the draft videos

    # Get the uploads playlist ID of the channel
    channels_response = service.channels().list(
        part='contentDetails', mine=True).execute()
    uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    nextPageToken = None
    while True:
        playlistitems_response = service.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='snippet',
            maxResults=50,
            pageToken=nextPageToken
        ).execute()

        # Fetch video details and check if it's a draft
        for item in playlistitems_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_response = service.videos().list(
                part='snippet,status',
                id=video_id
            ).execute()
            print(video_response['items'][0]['status'])
            status = video_response['items'][0]['status']
            if (status['privacyStatus'] == 'private'):
                # if 'publishAt' not in status:
                schedule_video(service, video_id, timecount)
                timecount += 1

        nextPageToken = playlistitems_response.get('nextPageToken')

        if nextPageToken is None:
            break

    print(videos)


def schedule_video(service, video_id, timecount):
    now = datetime.now()
    daycount = timecount // 3
    timecount = timecount % 3
    scheduledTime = datetime(now.year, now.month, now.day, 6, 0)
    if (timecount == 0):
        scheduledTime = datetime(now.year, now.month, now.day, 6, 0)
        scheduledTime = scheduledTime + timedelta(days=daycount)
    if (timecount == 1):
        scheduledTime = datetime(now.year, now.month, now.day, 12, 0)
        scheduledTime = scheduledTime + timedelta(days=daycount)
    if (timecount == 2):
        scheduledTime = datetime(now.year, now.month, now.day, 18, 0)
        scheduledTime = scheduledTime + timedelta(days=daycount)

    publish_time = scheduledTime.isoformat() + '.000Z'

    body = {
        'id': video_id,
        'status': {
            'publishAt': publish_time,
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False,
        }
    }

    service.videos().update(part='status', body=body).execute()
    print(f"Video {video_id} scheduled for {publish_time}")


if __name__ == '__main__':
    main()
