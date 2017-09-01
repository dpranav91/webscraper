'''
    This script will attempt to open your webbrowser,
    perform OAuth 2 authentication and print your access token.
    It depends on two libraries: oauth2client and gflags.
    To install dependencies from PyPI:
    $ pip install python-gflags oauth2client
    Then run this script:
    $ python get_oauth2_token.py

    This is a combination of snippets from:
    https://developers.google.com/api-client-library/python/guide/aaa_oauth
'''

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.file import Storage

CLIENT_ID = '937657066847-lbb5fic1fr6rdpi685u5db7h7elpcind.apps.googleusercontent.com'
CLIENT_SECRET = '8J6OjRF9CX1VY5qiIpM7_OUo'

flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           scope='https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
                           redirect_uri='http://example.com/auth_return')

storage = Storage('creds.data')

credentials = run_flow(flow, storage)
print(credentials)
print("access_token: %s" % credentials.access_token)