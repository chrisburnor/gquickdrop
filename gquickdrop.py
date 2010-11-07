from dropbox.auth import Authenticator
from dropbox.client import DropboxClient

import webbrowser, sys

class FileAlreadyPresentError(Exception):
    def __init__(self, fileName):
        self.fileName = fileName
        
    def __str__(self):
        return repr(self.fileName)
    
def getAccToken(reqToken):
    print "Getting Authorization Token"
    ######################################################
    # Need to replace this with gtkmozembed from pygtk.com
    webbrowser.open(auth.build_authorize_url(reqToken))
    raw_input("\nPress Enter when you have authorized   \n")
    ######################################################
    accToken = auth.obtain_access_token(reqToken, "")
    return accToken

def openClient():
    config = Authenticator.load_config("config.ini")
    auth = Authenticator(config)
    reqToken = auth.obtain_request_token()
    accToken = getAccToken(reqToken)
    print "Token: %s" % str(accToken)
    client = DropboxClient("api.dropbox.com", "api-content.dropbox.com", 80, auth, accToken)
    
    return client
    
def uploadFile(fileName, client):
    print "Uploading %s" % fileName
    fp = open(fileName, "r")
    resp = client.put_file("dropbox", "/Public", fp);
    fp.close()
    
def getPublicUrl(fileName, client):
    fileMetaData = client.metadata("dropbox", "/Public/%s" % fileName)
    publicUrl = fileMetaData['path']
    return publicUrl
    

if __name__ == "__main__":
    try:
        myFile = sys.argv[1]
    except IndexError:
        print "Error, you must specify a file to upload"
    else:
        client = openClient()
        
        public = client.metadata("dropbox", "/Public")
        if public.status != 404:
            print "Loaded Public directory   "
            try:
                for pubFile in public.data['contents']:
                    if pubFile['path'].split("/")[-1] == myFile:
                        raise FileAlreadyPresentError(myFile)
            except FileAlreadyPresentError as e:
                print "File %s already present" % e.fileName
            else:
                print "File Not Present"
                uploadFile(myFile, client)
            print "File URL: %s" % getPublicUrl(e.fileName, client)
        
                        
        else:
            print "Public directory not found"
    

