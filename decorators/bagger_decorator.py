from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
import json

# def role(allowed_role=['']):
#     def decorator(func):
#         def wrap(request, *args, **kwargs):
#             jsonData = json.loads(request.body.decode('utf-8'))
#             role = jsonData['role']
#             if role in allowed_role:
#                 return func(request, *args, **kwargs)
#             else:
#                 raise PermissionDenied
#         return wrap
#     return decorator