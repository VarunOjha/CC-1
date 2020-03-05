import boto3
import json
import decimal


def create_es_documents(obj):
    res = {}
    res["id"] = obj['id']
    res['categories'] = obj["categories"]
    return res

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

def fetch_items():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Yelp-Restaurants')
    response = table.scan(Limit=100)
    data = response['Items']
    # print(response)
    # print("\n\n Size of the itemset")
    print(json.dumps(replace_decimals(create_es_documents(data[0]))))
    return
    i = 0

    while 'LastEvaluatedKey' in response:
        print("i=>",i)
        i+=1
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'],Limit=100)
        data.extend(response['Items'])

fetch_items()