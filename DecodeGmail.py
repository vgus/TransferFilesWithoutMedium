import base64
from MethodsGmail import getGmailEncodedMessages
from googleapiclient.errors import HttpError


def main(emailSubject):
    
    index = -1
    contentProblem = False
    problems = []
    lastContent = ''
    content = ''

    try:
        messages = getGmailEncodedMessages(emailSubject)
    except HttpError as error:
        contentProblem = True
        problems.append((f'An API error occurred: {error}'))
    for message in messages:
        if index > message['index']:
            contentProblem = True
            problems.append('Content disordered')
        elif index == message['index'] and lastContent != message['info']:
            contentProblem = True
            problems.append("Duplicate index and the message content is not similar")
        elif index+1 < message['index']:
            contentProblem = True
            problems.append('Missing element: '+str(index+1))
            index = message['index']-1
        else:
            content += message['info']
        lastContent = message['info']
        index += 1 
    
    if contentProblem:
        print('A problem ocurred:', *problems,sep='\n')
    else:
        with open(emailSubject, "wb") as file:
            decoded_string = base64.b64decode(content)
            file.write(decoded_string)

if __name__ == '__main__':
    emailSubject = "19.zip"
    
    main(emailSubject)

            
