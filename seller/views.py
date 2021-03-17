from os import name
from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from .models import *
from django.contrib.auth import authenticate
from utilities.jwt import JWTClass

decorator_ = DecoratorHandler()
jwt_ = JWTClass()


#Add Product
@decorator_.rest_api_call(allowed_method_list=['POST'])
def add_vendor(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message="Please fill all the values").return_response_object()
    
    full_name_ = data['full_name']
    email_address_ = data['email_address']
    phone_number_ = data['phone_number']
    company_ = data['company']
    role_ = data['role']

    if role_.upper().strip() != "VENDOR":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User role is not valid").return_response_object()
    
    if Vendor.objects.filter(email_address=email_address_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User email already exists").return_response_object()
    
    if Vendor.objects.filter(phone_number=phone_number_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User phone number already exists").return_response_object()
    else:
        Vendor.objects.create(full_name=full_name_, email_address=email_address_, phone_number=phone_number_, company=company_)
        return SuccessResponse(message='Vendor Created Successfully').return_response_object()