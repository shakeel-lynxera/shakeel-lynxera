import json


def get_request_obj(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST
    return data
