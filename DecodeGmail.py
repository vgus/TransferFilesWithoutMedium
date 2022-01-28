import base64
from MethodsGmail import getGmailEncodedMessages, setReadMessages
from googleapiclient.errors import HttpError
from sys import argv


def main(emailSubject):
    
    index = -1
    contentProblem = False
    problems = []
    lastContent = ''
    content = ''
    print('Getting messages...')
    try:
        messages = getGmailEncodedMessages(emailSubject)
        if not messages:
            contentProblem = True
            problems.append(f"No messages with subject {emailSubject} found.")
    except HttpError as error:
        contentProblem = True
        problems.append((f'An API error occurred: {error}'))
    for message in messages:
        if index > message['index']:
            contentProblem = True
            problems.append('Content disordered')
        elif index == message['index'] and lastContent != message['info']:
            contentProblem = True
            problems.append(f"Duplicate index at {message['index']} and the message content is not similar")
        elif index == message['index']:
            print(f"Warning: Duplicate message at index {message['index']}")
            index -= 1
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
        print("Triyin to make the file...")
        with open(emailSubject, "wb") as file:
            decoded_string = base64.b64decode(content)
            file.write(decoded_string)
            print(f"File {emailSubject} created.")
        try:
            setReadMessages(list(map(lambda i: i['id'],messages)))
            print("Unread and archive messages")
        except HttpError as error:
            print("It can't set Unread and archive messages:"+error)


if __name__ == '__main__':
    #emailSubject = "21.zip"
    emailSubject = argv[1]
    main(emailSubject)

            
