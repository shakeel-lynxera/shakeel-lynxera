from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from .models import *
from django.contrib.auth import authenticate
from utilities.jwt import JWTClass

decorator_ = DecoratorHandler()
jwt_ = JWTClass()


@decorator_.rest_api_call(allowed_method_list=['POST'])
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email'].lower().strip()
    password = data['password']
    role = data['role'].upper().strip()
    name = data['name']

    if not Role.objects.filter(name=role).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()

    if User.objects.filter(email__iexact=email).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This email address already exists').return_response_object()

    user_ = User.objects.create(email=email, username=email, first_name=name)
    user_.set_password(password)
    user_.save()
    UserProfile.objects.create(name=name, user=user_)
    UserRole.objects.create(user=user_, role=Role.objects.get(name=role))
    return SuccessResponse(message='User is successfully created').return_response_object()


@decorator_.rest_api_call(allowed_method_list=['POST'])
def login(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email'].lower().strip()
    password = data['password']

    user = authenticate(username=email, password=password)
    if user:
        token = jwt_.create_user_session(user)
        return SuccessResponse(data={'token': token}).return_response_object()

    else:
        return FailureResponse(message='Invalid username or password',
                               status_code=BAD_REQUEST_CODE).return_response_object()