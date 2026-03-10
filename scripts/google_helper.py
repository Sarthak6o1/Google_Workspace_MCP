import os
import os.path
from urllib.parse import urlparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

try:
    # In LibreChat, GOOGLE_* vars are usually passed in the process env.
    # We still try to load a local .env when running this script directly,
    # but ignore malformed entries instead of crashing the MCP server.
    load_dotenv()
except ValueError:
    pass

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/chat.spaces',
    'https://www.googleapis.com/auth/chat.messages',
    'https://www.googleapis.com/auth/chat.memberships',
    'https://www.googleapis.com/auth/chat.messages.reactions',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/forms.responses.readonly',
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/cse'
]

DEFAULT_REDIRECT_URI = "http://localhost:8080/"


def _get_local_redirect_uri():
    redirect_uri = (
        os.getenv('GOOGLE_MCP_REDIRECT_URI')
        or os.getenv('GOOGLE_REDIRECT_URI')
        or DEFAULT_REDIRECT_URI
    )

    parsed = urlparse(redirect_uri)
    if parsed.scheme != 'http' or parsed.hostname not in ('localhost', '127.0.0.1'):
        return DEFAULT_REDIRECT_URI

    return redirect_uri


def _get_local_redirect_port(redirect_uri):
    parsed = urlparse(redirect_uri)
    return parsed.port or 80

def get_credentials():
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
            client_id = os.getenv('GOOGLE_CLIENT_ID')
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

            if not client_id or not client_secret:
                raise ValueError("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in environment")

            config = {
                "web": {
                    "client_id": client_id,
                    "project_id": "naomedical-workspace-v1",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": client_secret,
                    "redirect_uris": [_get_local_redirect_uri()]
                }
            }

            local_redirect = _get_local_redirect_uri()
            local_port = _get_local_redirect_port(local_redirect)

            flow = InstalledAppFlow.from_client_config(config, SCOPES, redirect_uri=local_redirect)

            # Force localhost so Google uses the redirect URI registered in GCP.
            creds = flow.run_local_server(
                host='localhost',
                port=local_port,
                prompt='consent',
                open_browser=True,
            )
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_service(service_name, version):
    creds = get_credentials()
    return build(service_name, version, credentials=creds)
