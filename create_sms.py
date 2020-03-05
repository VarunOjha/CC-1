import json
import boto3
import requests 
import time
import decimal
from boto3.dynamodb.conditions import Key, Attr

SEARCH_URL = "https://search-restaurant-gunm43fjnatwo3gdrulwwsgsqa.us-east-1.es.amazonaws.com/restaurants/_search"

def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(0,len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
        # In my original code I'm converting to int or float, comment the line above if necessary.
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


def get_restaurants(ids):
	print(ids)
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('Yelp-Restaurants')
	response = table.get_item(Key={'id': ids}, TableName='Yelp-Restaurants')
	# print("\n\n")
	response = replace_decimals(response)
	print(response)
	nameAddress = " "+response['Item']['name'] + ","
	for i in range(0,len(response['Item']['location']['display_address'])):
		nameAddress += response['Item']['location']['display_address'][i] + " "
	return nameAddress



def search_restaurants_for_cuisine(cuisine):
	requestBody = {}
	requestBody['size'] = 3
	requestBody['query'] = {}
	requestBody['query']['match_phrase'] ={}
	requestBody['query']['match_phrase']['categories.title'] = cuisine
	headers = {'Content-type': 'application/json'}
	# print(json.dumps(requestBody))
	r = requests.get(url = SEARCH_URL,data=json.dumps(requestBody),headers=headers)
	data = r.json()
	# print("\n\n\n\n")
	return data['hits']['hits']

def get_sqs_entries():
	sqs = boto3.client('sqs')
	m = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/146486855224/Dining.fifo')
	messageId = m['Messages'][0]['MessageId']
	receiptHandle = m['Messages'][0]['ReceiptHandle']
	x = json.loads(m['Messages'][0]['Body'])
	# print("messageId =>",messageId)
	# print("receiptHandle =>",receiptHandle)
	sqs.delete_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/146486855224/Dining.fifo', ReceiptHandle=receiptHandle)
	return x['slots']
	

slots = get_sqs_entries()
# print(slots)
rests = search_restaurants_for_cuisine(slots['Cuisine'])
# print(json.dumps(rests))


message = "Hello! Here are the "+slots['Cuisine']+ " suggestions for "+slots['Size']+" people for "+slots['Date']
message += " at "+slots['Time'] + " :"
# print("\n\n\n message =>")
# print(message)
for i in range(0,len(rests)):
	message += "(" + str(i+1) + ")" + get_restaurants(rests[i]['_source']['id'])

message += ". Enjoy your meal"
print("\n\n\n message =>")
print(message)

sns = boto3.client('sns')
x = sns.publish(PhoneNumber = slots['Phone'], Message=message )