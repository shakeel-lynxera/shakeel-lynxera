from os import name
from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from .models import *
from django.contrib.auth import authenticate
from utilities.jwt import JWTClass
import string
import random
from random import randint
from django.core.mail import send_mail
from datetime import datetime, timedelta
import datetime as dt
from dateutil import parser
import pytz

utc=pytz.UTC
decorator_ = DecoratorHandler()
jwt_ = JWTClass()


@decorator_.rest_api_call(allowed_method_list=['POST'])
def register(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = json.loads(request.body.decode())
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
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = json.loads(request.body.decode())
    email = data['email'].lower().strip()
    password = data['password']

    user = authenticate(username=email, password=password)
    if user:
        token = jwt_.create_user_session(user)
        return SuccessResponse(data={'token': token}).return_response_object()

    else:
        return FailureResponse(message='Invalid username or password',
                               status_code=BAD_REQUEST_CODE).return_response_object()

#Seller Registration
@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_seller(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = json.loads(request.body.decode())
    email_ = data['email'].lower().strip()
    password_ = data['password']
    role_ = data['role'].upper().strip()
    shop_name_ = data['shop_name']
    phone_ = data['phone']
    address_ = data['address']

    #362 24/7 Always open in whole year
    is_always_open_ = data['is_always_open']

    #open and close shops duration per week
    monday_is_24hours_ = data['monday_is_24hours']
    monday_open_time_ = data['monday_open_time']
    monday_close_time_ = data['monday_close_time']

    tuesday_is_24hours_ = data['tuesday_is_24hours']
    tuesday_open_time_ = data['tuesday_open_time']
    tuesday_close_time_ = data['tuesday_close_time']

    wednesday_is_24hours_ = data['wednesday_is_24hours']
    wednesday_open_time_ = data['wednesday_open_time']
    wednesday_close_time_ = data['wednesday_close_time']

    thursday_is_24hours_ = data['thursday_is_24hours']
    thursday_open_time_ = data['thursday_open_time']
    thursday_close_time_ = data['thursday_close_time']

    friday_is_24hours_ = data['friday_is_24hours']
    friday_open_time_ = data['friday_open_time']
    friday_close_time_ = data['friday_close_time']

    saturday_is_24hours_ = data['saturday_is_24hours']
    saturday_open_time_ = data['saturday_open_time']
    saturday_close_time_ = data['saturday_close_time']

    sunday_is_24hours_ = data['sunday_is_24hours']
    sunday_open_time_ = data['sunday_open_time']
    sunday_close_time_ = data['sunday_close_time']


    if not Role.objects.filter(name=role_).exists() or role_.upper().strip() != "SELLER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()

    if User.objects.filter(email__iexact=email_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This email address already exists').return_response_object()
    
    if UserProfile.objects.filter(phone_number=phone_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This phone number already exists').return_response_object()


    user_ = User.objects.create(email=email_, username=email_, first_name=shop_name_)
    user_.set_password(password_)
    user_.save()
    profileObj_ = UserProfile.objects.create(name=shop_name_, user=user_, phone_number = phone_,address=address_, is_set_password=True)
    roleObj_ = UserRole.objects.create(user=user_, role=Role.objects.get(name=role_))

    shopHourObj = ShopHour.objects.create(is_always_open=is_always_open_, week=
                                                        {
                                                        'days':[
                                                                {
                                                                    'name':'monday',
                                                                    'is_24hours':monday_is_24hours_,
                                                                    'open_time':monday_open_time_,
                                                                    'close_time':monday_close_time_, 
                                                                },
                                                                {
                                                                    'name':'tuesday',
                                                                    'is_24hours':tuesday_is_24hours_,
                                                                    'open_time':tuesday_open_time_,
                                                                    'close_time':tuesday_close_time_, 
                                                                },
                                                                {
                                                                    'name':'wednesday',
                                                                    'is_24hours':wednesday_is_24hours_,
                                                                    'open_time':wednesday_open_time_,
                                                                    'close_time':wednesday_close_time_, 
                                                                },
                                                                {
                                                                    'name':'thursday',
                                                                    'is_24hours':thursday_is_24hours_,
                                                                    'open_time':thursday_open_time_,
                                                                    'close_time':thursday_close_time_, 
                                                                },
                                                                {
                                                                    'name':'friday',
                                                                    'is_24hours':friday_is_24hours_,
                                                                    'open_time':friday_open_time_,
                                                                    'close_time':friday_close_time_, 
                                                                },
                                                                {
                                                                    'name':'saturday',
                                                                    'is_24hours':saturday_is_24hours_,
                                                                    'open_time':saturday_open_time_,
                                                                    'close_time':saturday_close_time_, 
                                                                },
                                                                {
                                                                    'name':'sunday',
                                                                    'is_24hours':sunday_is_24hours_,
                                                                    'open_time':sunday_open_time_,
                                                                    'close_time':sunday_close_time_, 
                                                                },
                                                                ]
                                                        }
    )
    Seller.objects.create(user=user_, profile=profileObj_, role=roleObj_, shopHour=shopHourObj)
    return SuccessResponse(message='Seller is successfully created').return_response_object()



#Driver Registration
@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_driver(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = json.loads(request.body.decode())
    email_ = data['email'].lower().strip()
    password_ = data['password']
    role_ = data['role'].upper().strip()
    name_ = data['name']
    phone_ = data['phone']
    address_ = data['address']
    dob_ = data['dob']
    social_security_number_ = data['social_security_number']

    vehicle_type_ = data['vehicle_type']
    vehicle_make_ = data['vehicle_make']
    vehicle_color_ = data['vehicle_color']
    vehicle_number_ = data['vehicle_number']

    license_state_ = data['license_state']
    license_number_ = data['license_number']
    license_exp_date_ = data['license_exp_date']


    if not Role.objects.filter(name=role_).exists() or role_.upper().strip() != "DRIVER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()

    if User.objects.filter(email__iexact=email_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This email address already exists').return_response_object()
    
    if UserProfile.objects.filter(phone_number=phone_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This phone number already exists').return_response_object()
    
    if Driver.objects.filter(social_security_number=social_security_number_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This social security number already exists').return_response_object()
    
    if Vehicle.objects.filter(vehicle_number__iexact=vehicle_number_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This vehicle number already exists').return_response_object()
    
    if License.objects.filter(license_number=license_number_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This License number already exists').return_response_object()
    


    user_ = User.objects.create(email=email_, username=email_, first_name=name_)
    user_.set_password(password_)
    user_.save()
    licenseObj_ = License.objects.create(license_state=license_state_, license_number=license_number_, license_exp_date=license_exp_date_)
    vehicleObj_ = Vehicle.objects.create(vehicle_type=vehicle_type_, vehicle_make=vehicle_make_, vehicle_number=vehicle_number_, vehicle_color=vehicle_color_)
    profileObj_ = UserProfile.objects.create(name=name_, user=user_, date_of_birth=dob_, phone_number = phone_,address=address_, is_set_password=True)
    roleObj_ = UserRole.objects.create(user=user_, role=Role.objects.get(name=role_))
    Driver.objects.create(social_security_number=social_security_number_, user=user_, vehicle=vehicleObj_, profile=profileObj_, role=roleObj_, license=licenseObj_)
    return SuccessResponse(message='Driver is successfully created').return_response_object()


#Buyer Registration
@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_buyer(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = json.loads(request.body.decode())
    email = data['email'].lower().strip()
    role = data['role'].upper().strip()
    address = data['address']
    password = data['password']

    if not Role.objects.filter(name=role).exists() or role.upper().strip() != "BUYER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()
    
    if User.objects.filter(email__iexact=email).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This email address already exists').return_response_object()

    user_ = User.objects.create(email=email, username=email)
    user_.set_password(password)
    user_.save()

    UserProfile.objects.create(user=user_, address=address, is_set_password=True)
    UserRole.objects.create(user=user_, role=Role.objects.get(name=role))

    #Directly login
    user = authenticate(username=email, password=password)
    if user:
        token = jwt_.create_user_session(user)
        return SuccessResponse(data={'token': token}).return_response_object()
    return FailureResponse(status_code=BAD_REQUEST_CODE, message='Invalid username or password').return_response_object()


#Send verification code to Email for Reset Password
@decorator_.rest_api_call(allowed_method_list=['POST'])
def send_verification_code_for_reset_password(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = json.loads(request.body.decode())
    email = data['email'].lower().strip()

    if User.objects.filter(email__iexact=email).exists():
        timeNow = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
        timeExpire = dt.datetime.strftime(dt.datetime.now() + dt.timedelta(seconds=30), "%Y-%m-%d %H:%M:%S")
        user = User.objects.get(email=email)

        if ResetPassword.objects.filter(user=user).exists():
            resetObj = ResetPassword.objects.get(user=user)
            if resetObj.key_expires < utc.localize(parser.parse(timeNow)):
                verification_code = ''
                for _ in range(6):
                    verification_code += str(randint(1, 9))
                send_mail(
                    'kwk | Verification Code',
                    verification_code,
                    'fitstarproo@gmail.com',
                    [email],
                    fail_silently=False,
                )
                resetObj.verification_code = verification_code
                resetObj.key_expires = timeExpire
                resetObj.save()
                return SuccessResponse(message='Verification code resent on email').return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message='Please wait for few seconds').return_response_object()

        verification_code = ''
        for _ in range(6):
            verification_code += str(randint(1, 9))
        send_mail(
            'kwk | Verification Code',
            verification_code,
            'fitstarproo@gmail.com',
            [email],
            fail_silently=False,
        )
        ResetPassword.objects.create(user=user, verification_code=verification_code, key_expires=timeExpire)
        return SuccessResponse(message='Verification code sent on email').return_response_object()
    return FailureResponse(status_code=BAD_REQUEST_CODE, message='Invalid email does not exists').return_response_object()
    

#Validate verification code for Reset Password
@decorator_.rest_api_call(allowed_method_list=['POST'])
def validate_verification_code_for_reset_password(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = json.loads(request.body.decode())
    verification_code = str(data['verification_code'])
    if ResetPassword.objects.filter(verification_code__iexact=verification_code).exists():
        mObject = ResetPassword.objects.get(verification_code = verification_code)
        return SuccessResponse({"email" : mObject.user.email}, message='verificaton code matched').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='Invalid code').return_response_object()


#Reset Password
@decorator_.rest_api_call(allowed_method_list=["POST"])
def reset_password(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = json.loads(request.body.decode())
    email = data['email']
    password = data['password']
    timeNow = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
    if User.objects.filter(email__iexact=email).exists():
        user_ = User.objects.get(email = email)
        if ResetPassword.objects.filter(user=user_).exists():
            resetObj = ResetPassword.objects.get(user = user_)
            if resetObj.key_expires < utc.localize(parser.parse(timeNow)):
                resetObj.delete()
                return SuccessResponse(message='Verification code expired').return_response_object()
            else:
                user_.set_password(password)
                user_.save()
                resetObj.delete()
                return SuccessResponse(message='Password reset successfully').return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='Generate another OTP').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='Invalid email').return_response_object()