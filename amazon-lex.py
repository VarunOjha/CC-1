import json
import boto3
import requests 

URL = 'https://tx9xfdyz8h.execute-api.us-east-1.amazonaws.com/dev/chatbot'


def chatbot(message):
    myobj = {}
    myobj['BotRequest'] = []
    myobj['BotRequest'].append({'Message':message})
    print(json.dumps(myobj))
    x = requests.post(url=URL, data = json.dumps(myobj))
    print(x.text)



message = input("Enter a message :")
chatbot(message)

    


