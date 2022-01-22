import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64decode



def getGmailService(SCOPES):
    '''
        It retrieves a Gmail service to use the API depending the scope 
    ''' 
    if os.path.exists('secrets/token.json'):
        creds = Credentials.from_authorized_user_file('secrets/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('secrets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('secrets/token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Build the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service

def getinformationFromMessage(message):
    '''
        Get the encoded string from a message 
    '''
    sal = {}
    partition = message.split('\n')
    try:
        sal['index'] = int(partition[0])
        sal['info'] = partition[1].rstrip()
        return sal
    except:
        return {}

def getGmailEncodedMessages(subject):
    '''
        Retrieve all messages from a Gmail account that matches the subject and be part of an encoded message.
        Return a list of messages orderer by the index of the encoded messages
    '''
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    messagesInThread = []
    service = getGmailService(SCOPES)
    messages = service.users().messages().list(userId='me', q=f'subject:{subject}').execute().get('messages', [])
    for message in messages:        
        tdata = service.users().messages().get(userId='me', id=message['id']).execute()
        mimetype = tdata['payload']['mimeType']
        msg = tdata['payload']['body']['data']        
        msgDecoded = urlsafe_b64decode(msg).decode()
        #print(message)
        if mimetype == 'text/plain':
            info = getinformationFromMessage(msgDecoded)
            if info:
                message.update(info) 
                messagesInThread.append(message)
    return sorted(messagesInThread, key= lambda i: i['index'])     

def setReadMessages(messages):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

if __name__ == '__main__':

    print(getGmailEncodedMessages('21.zip'))
    message = '''21
VYfnygQXTfwyvqV8UKmcoTJIlL6Foembnoh0XH0UV516FcjvUIIPqAmwKpAUaDtOk7v6ChiFHHR9nIWlKxtWHJIh1sW9rYOEjxXP7d/oAM9sngID3barF4rUBuqzuaZxA8U6zyqvgEs/8IyraiwaX7NMORG3dP1F6O3sCFgs036lKLUqplNC+YVXtYOFIlnWoOKszTyW6wngMbJ2Co3f7PZVU76iyxoKHhhsmallNP0+DIMj8Dqb3IDXLsSfqqXDAusmtHVSRT4FcDyTtyo269VxA2788/0u6T5tg02PIWc2smB8/Nd9j7/XT5EZBXuJiBu3M9uZJzMjE9Px86CgloMEWxPkjB2c0IhaBa3quoHS7SYtf4VVZGtFvL6IobdXx9cvsl992C6cOWeNCqg+UmsZy3PNEiuX6WskaGcniAy6Nh4W6uhvIHcxl5nThtRkJCfWMxNocz3+XgN1ylbpCZEINBb94rwy+HcVkULJWHnHMtGyDuAr8l+hapW4eKCX19Tktm0ViB7zKXguNoqdnQ2iW8NsIgpaq2lQSwECLQAUAAEACADlg3BTvABNAmh6AADXjQAALwAkAAAAAAAAACAAAAAAAAAAUERGL0tfRjAwMTM4MzQwMjAyMTIwMjExMTEyMTU0MDUxMDAyMDIxMjcyMC5wZGYKACAAAAAAAAEAGAAUq0WoOdvXAdBh+ac529cB0GH5pznb1wFQSwECLQAUAAEACACogXBTIgZcU6oNAAD6GAAALwAkAAAAAAAAACAAAADZegAAWE1ML0tfRjAwMTM4MzQwMjAyMTIwMjExMTEyMTU0MDUxMDAyMDIxMjcyMC54bWwKACAAAAAAAAEAGABtgNwnN9vXAY8MqCc329cBjwyoJzfb1wFQSwUGAAAAAAIAAgACAQAA9IgAAAAA


Saludos,
Ing. Uriel Vidal'''
    #print(getinformationFromMessage(message))