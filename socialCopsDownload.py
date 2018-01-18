try:
    import sys
    import mimetypes
    from os import stat
    from pathlib import Path
    import os
    from apiclient.discovery import build
    from apiclient.http import MediaFileUpload,MediaIoBaseDownload
    from httplib2 import Http
    from oauth2client import file, client,tools
    import io
    import time
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


def str2float(string):
    for char in string:
        if char not in ['0','1','2','3','4','5','6','7','8','9']:
            string=string.strip(char)
    return string

def syncFolder(DRIVE):
    response = DRIVE.files().list(q="mimeType='application/vnd.google-apps.folder'"and"name='socialCopsFolderSync'",
        spaces='drive').execute()
    for file in response.get('files', []):
        print ('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
        folder=file
        break

    parentFolderId=folder.get('id')
    page_token=None
    Q=("'"+str(parentFolderId)+"'"+' in parents')
    response = DRIVE.files().list(q=Q,spaces='drive',fields='nextPageToken, files(id, name)',
        pageToken=page_token).execute()
    for file in response.get('files', []):
        if file.get('name')=="logs":
            pass
        else:
            request = DRIVE.files().get_media(fileId=file.get('id'))
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
    print("Done!!!>")

localLogs=open('logs.txt','r')
lastModifiedLocalTime=localLogs.readline()
lastModifiedLocalTime=float(str2float(lastModifiedLocalTime))
localLogs.close()


page_token = None
response = DRIVE.files().list(q="mimeType='application/vnd.google-apps.document'"and"name='logs'",
                                              spaces='drive').execute()
for file in response.get('files', []):
    logs=file
    break
while True:
    file_id = logs.get('id')
    MIMETYPE='text/plain'
    #request ,data= DRIVE.files().get_media(fileId=file_id).execute()
    data = DRIVE.files().export(fileId=file_id, mimeType=MIMETYPE).execute()
    if data:
        fn = 'logs.txt'
        with open(fn, 'wb') as fh:
            fh.write(data)
        fh.close()

    serverLogs=open('logs.txt','r+')
    lastModifiedServerTime=serverLogs.readline()
    serverLogs.close()
    lastModifiedServerTime=float(str2float(lastModifiedServerTime))
    if(lastModifiedServerTime>lastModifiedLocalTime):
        print("Update found.")
        syncFolder(DRIVE)
        lastModifiedLocalTime=lastModifiedServerTime
        print("KUDOS : Update Complete")
        print("\n\n***Automatic Updates are active***")
        print("          ***BEHOLD***            ")
    else:
        print("No new updates.")

    time.sleep(5)
