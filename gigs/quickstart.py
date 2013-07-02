#!/usr/bin/python

import httplib2
import pprint
import os,sys

#Settings are imported 
#because environment variable DJANGO_SETTINGS_MODULE is not defined
path=os.path.dirname(os.path.abspath(__file__))
path=os.path.join(path,'..')
sys.path.insert(0,path)
os.environ['DJANGO_SETTINGS_MODULE']='settings'



from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

from mezzanine.conf import settings


# Copy your credentials from the APIs Console
CLIENT_ID = settings.GOOGLE_CLIENT_ID
CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET


# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
#REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
REDIRECT_URI = 'http://localhost:8000'

# Path to the file to upload
FILENAME = '/Users/elmahdibouhram/job_connector/gigs/document.txt'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()

credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)


drive_service = build('drive', 'v2', http=http)

# Insert a file
media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
body = {
  'title': 'My document',
  'description': 'admin',
  'mimeType': 'text/plain'
}

file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file)