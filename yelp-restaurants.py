import requests
import boto3
from decimal import Decimal
import time
# Decimal(f)
def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(0,len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj
def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}

def populate_restaurants(location,offset,limit):
    client = boto3.resource('dynamodb')
    headers = {"Authorization": "Bearer R2lU6gGIPQiJ9VqxJtBsF3nACHWuIE8JoVMBot9o0JfvA1kezaPXuS3N1XZhrK-Yt3_xFdKNB0HSVxcZCUew5BEhu7OuRmpFg8ocY60DYLqpW4PsRpE9m-lYC41IXnYx"}

    URL = "https://api.yelp.com/v3/businesses/search"
    p = {'location':location,'limit':limit,'offset':offset}
    print("This is url")
    print(URL)
    r = requests.get(url = URL,params=p,headers=headers)
    data = r.json()

    print(data)

    print("\n\n Count")
    print(len(data["businesses"]))
    print(data)

    table = client.Table('Yelp-Restaurants')
    print(table.creation_date_time)

    print("\n\n\n")
    for inst in data['businesses']:
        inst = replace_decimals(inst)
        inst = clean_empty(inst)
        print(inst)
        table.put_item(Item=inst)

location = input("Enter a location:")
offset = 0
while offset < 1000:
    print("\n\n in iteration =>",offset)
    populate_restaurants(location,offset,50)
    offset+=50
    time.sleep(1)