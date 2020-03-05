import json
import boto3
import requests 
import time

URL = 'https://xu5gmm9tyg.execute-api.us-east-1.amazonaws.com/dev/chatbot'


def chatbot(message):
    myobj = {}
    myobj['BotRequest'] = []
    myobj['BotRequest'].append({'Message':message})
    print(json.dumps(myobj))
    x = requests.post(url=URL, data = json.dumps(myobj))
    print(x.text)




chatbot("Hello")
time.sleep(1)
chatbot("I need some restaurant suggestions")
time.sleep(1)
chatbot("NYC")
time.sleep(1)
chatbot("Italian")
time.sleep(1)
chatbot("2")
time.sleep(1)
chatbot("Today")
time.sleep(1)
chatbot("5.00 pm")
time.sleep(1)
chatbot("+1 929 414 9882")

    


