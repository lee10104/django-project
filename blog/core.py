from django.http import HttpResponse
import json

def upload_path(instance, filename):
    return "{category}/{filename}".format(category=instance.category.name, filename=filename)

def send_http_response(info):
    return HttpResponse(json.dumps(info), 'application/json')
