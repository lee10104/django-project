from django.http import HttpResponse
from .keys import *
import json
import oauth2

def upload_path(instance, filename):
    return "{category}/{filename}".format(category=instance.category.name, filename=filename)

def send_http_response(info):
    return HttpResponse(json.dumps(info), 'application/json')

def remove_indents(s):
    return s.replace('\t', '').replace('\n', '').replace('\r', '')

def oauth_request(consumer_key, consumer_secret, access_token, access_token_secret):
    try:
        consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth2.Token(key=access_token, secret=access_token_secret)
        client = oauth2.Client(consumer, token)
        return client
    except Exception as e:
        print(e)
        return None

def get_response_from_twitter_api(end_node, arg_dict):
    client = oauth_request(Twitter.CONSUMER_KEY, Twitter.CONSUMER_SECRET, Twitter.ACCESS_TOKEN, Twitter.ACCESS_TOKEN_SECRET)
    base = 'https://api.twitter.com/1.1/'
    url = base + end_node
    if arg_dict:
        url += '?'
        for key in arg_dict.keys():
            url += key + '=' + arg_dict[key] + '&'
        url = url[:-1]

    response, data = client.request(url)
    try:
        if response['status']:
            response = {'status': response['status']}
            response['data'] = json.loads(data.decode('utf-8'))
            return response
        else:
            return None
    except Exception as e:
        print(e)
        return None
