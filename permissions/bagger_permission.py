from rest_framework.permissions import BasePermission
from model.models import mUser

class Bagger_Role(BasePermission):
    def has_permission(self, request, view):
        allowed_roles = [1,2,3]
        if request.method == "GET":
            return True
        elif request.method == "POST":
            if request.data.get('role') in allowed_roles:
                return True
        elif request.method == "PUT":
            if request.data.get('role') in allowed_roles:
                userId = request.data.get('id')
                user = mUser.objects.get(id=userId)
                if user is not None:
                    return True
                else:
                    return False
        elif request.method == "DELETE":
            return False