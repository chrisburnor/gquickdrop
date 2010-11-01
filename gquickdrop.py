from dropbox.auth import Authenticator
from dropbox.client import DropboxClient

import webbrowser

def openClient():
    config = Authenticator.load_config("config.ini")
    auth = Authenticator(config)
    reqToken = auth.obtain_request_token()
    print "Getting Authorization Token"
    webbrowser.open(auth.build_authorize_url(reqToken))
    raw_input("\nPress Enter when you have authorized...\n")
    accToken = auth.obtain_access_token(reqToken, "")
    print "Token: %s" % str(accToken)
    client = DropboxClient("api.dropbox.com", "api-content.dropbox.com", 80, auth, accToken)
    
    return client

if __name__ == "__main__":
    client = openClient()
    publicMetadata = client.metadata("dropbox", "/Public")
    if publicMetadata != 404:
        print "Loaded Public directory..."
    else:
        print "Public directory not found..."
    

