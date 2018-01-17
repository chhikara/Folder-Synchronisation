#Made by Abhishek Chhikara (ionicabhishek@gmail.com)
#Upload

try:
    import sys
    import mimetypes
    from os import stat
    from pathlib import Path
    import os
    from apiclient.discovery import build
    from apiclient.http import MediaFileUpload
    from httplib2 import Http
    from oauth2client import file, client, tools
    from watchdog.observers import Observer
    from watchdog.events import RegexMatchingEventHandler,FileSystemEventHandler
    import time
    import re

except Exception as e:
    print (e)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

def checkFolder():
    page_token = None
    global folder
    while True:
        flag=True
        response = DRIVE.files().list(q="mimeType='application/vnd.google-apps.folder'"and"name='socialCopsFolderSync'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print ('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
            flag=False
            folder=file
            break
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    if flag:
        createFolder()

def createFolder():
    global folder
    file_metadata = {
    'name': 'socialCopsFolderSync',
    'mimeType': 'application/vnd.google-apps.folder'}
    file = DRIVE.files().create(body=file_metadata,
                                    fields='id').execute()
    folder=file

checkFolder()

def listLocalFiles():
    exceptions=["client_secret.json","storage.json"]
    allFiles=os.listdir(".")
    for file in allFiles:
        if file in exceptions:
            allFiles.remove(file)
    return allFiles

def delete_file(service, file_id):#Deletes folder
    try:
        service.files().delete(fileId=file_id).execute()
    except (errors.HttpError, error):
        print ('An error occurred: %s' % error)

def logRegister(DRIVE):
    fileTemp=open("logs.txt",'w+')
    fileTemp.write(str(time.time()))
    fileTemp.close()
    MIMETYPE='application/vnd.google-apps.spreadsheet'
    file_metadata={'name':'logs','mimeType': MIMETYPE}
    media = MediaFileUpload('logs.txt',
        mimetype='text/plain',resumable=False)
    file = DRIVE.files().create(body=file_metadata,media_body=media,
        fields='id').execute()
    print("logs")
logRegister(DRIVE)

srcPath='C:\\Users\\ionic\\Desktop\\socialCopsFolderSync\\'

class eventHandler(RegexMatchingEventHandler):

    def __init__(self, regexes=['^((?!logs).)*$'],ignore_regexes=[],
                 ignore_directories=False, case_sensitive=False):
        super().__init__()
        if case_sensitive:
            self._regexes = [re.compile(r) for r in regexes]
            self._ignore_regexes = [re.compile(r) for r in ignore_regexes]
        else:
            self._regexes = [re.compile(r, re.I) for r in regexes]
            self._ignore_regexes = [re.compile(r, re.I) for r in ignore_regexes]
        self._ignore_directories = ignore_directories
        self._case_sensitive = case_sensitive

    def on_any_event(self,event):
        print("Modification Encountered : Beginning synchronising process")
        global folder
        delete_file(DRIVE,folder.get("id"))
        createFolder()
        allFiles=listLocalFiles()
        for item in allFiles:
            temp=(item.split("."))
            name=temp[0]
            if len(temp)>1:
                mimeType=mimetypes.types_map['.'+str(temp[-1])]
            else:
                mimeType='None'
            file_metadata={'name':name,'parents':[folder.get('id')]}
            media = MediaFileUpload(str(item),
                mimetype=mimeType,resumable=False)
            file = DRIVE.files().create(body=file_metadata,media_body=media,
                fields='id').execute()
            print("File %s Uploaded" %str(item))

        print("Sync process complete.\n\n***Script is still running!***\n")
        


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = eventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


#RegexMatchingEventHandler(regexes=['.*'], ignore_regexes=['^\. ','^[.]'], ignore_directories=True, case_sensitive=False)

        #fileTemp=DRIVE.files().create(body={'title':'logs.txt','mimeType':'text/plain',
        #'parents':[folder.get('id'),'dateTime':]},fields='id').execute()
        #fileTemp.SetContentString(str(time.time()))
        #fileTemp.upload()