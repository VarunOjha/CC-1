import boto3
import requests
import json
import decimal


ELASTIC_SEARCH_URL = "https://search-restaurant-gunm43fjnatwo3gdrulwwsgsqa.us-east-1.es.amazonaws.com/"

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

def create_es_documents(obj):
    res = {}
    res["id"] = obj['id']
    res['categories'] = obj["categories"]
    return res

def index_to_elastic_search(obj):
	URL = ELASTIC_SEARCH_URL + "restaurants/_doc"
	headers = {'Content-type': 'application/json'}
	r = requests.post(url=URL, data = obj, headers=headers)
	print("data =>")
	print(r.json())

def check_elastic_search():
	r = requests.get(url = ELASTIC_SEARCH_URL)
	data = r.json()
	print("data =>")
	print(data)

def index_yelp_restaurants_dynamodb():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Yelp-Restaurants')
    response = table.scan(Limit=100)
    data = response['Items']
    i=0
    while i < len(data):
    	index_to_elastic_search(json.dumps(replace_decimals(create_es_documents(data[i]))))
    	i+=1
    

    # while 'LastEvaluatedKey' in response:
    #     print("i=>",i)
    #     i+=1
    #     response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'],Limit=100)
    #     data.extend(response['Items'])


index_yelp_restaurants_dynamodb()