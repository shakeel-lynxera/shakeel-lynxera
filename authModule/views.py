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
import json

utc=pytz.UTC
decorator_ = DecoratorHandler()
jwt_ = JWTClass()


# @decorator_.rest_api_call(allowed_method_list=['POST'])
# def register(request):
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#     except:
#         try:
#             data = json.loads(request.body.decode())
#         except:
#             data = request.POST

#     email = data['email'].lower().strip()
#     password = data['password']
#     role = data['role'].upper().strip()
#     name = data['name']

#     if not Role.objects.filter(name=role).exists():
#         return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()

#     if User.objects.filter(email__iexact=email).exists():
#         return FailureResponse(status_code=BAD_REQUEST_CODE, message='This email address already exists').return_response_object()

#     user_ = User.objects.create(email=email, username=email, first_name=name)
#     user_.set_password(password)
#     user_.save()
#     UserProfile.objects.create(name=name, user=user_)
#     UserRole.objects.create(user=user_, role=Role.objects.get(name=role))
#     return SuccessResponse(message='User is successfully created').return_response_object()


@decorator_.rest_api_call(allowed_method_list=['POST'])
def login(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

    email_ = data['email'].lower().strip()
    password_ = data['password']
    role_ = data['role']

    if not Role.objects.filter(name=role_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()

    if Role.objects.filter(name=role_).exists() or role_.upper().strip() != "SELLER":
        user = authenticate(username=email_, password=password_)
        if user:
            token = jwt_.create_user_session(user)
            return SuccessResponse(data={'token': token}).return_response_object()

        else:
            return FailureResponse(message='Invalid username or password',
                                status_code=BAD_REQUEST_CODE).return_response_object()

    elif Role.objects.filter(name=role_).exists() or role_.upper().strip() != "DRIVER":
        user = authenticate(username=email_, password=password_)
        if user:
            token = jwt_.create_user_session(user)
            return SuccessResponse(data={'token': token}).return_response_object()

        else:
            return FailureResponse(message='Invalid username or password',
                                status_code=BAD_REQUEST_CODE).return_response_object()

    elif Role.objects.filter(name=role_).exists() or role_.upper().strip() != "BUYER":
        user = authenticate(username=email_, password=password_)
        if user:
            token = jwt_.create_user_session(user)
            return SuccessResponse(data={'token': token}).return_response_object()

        else:
            return FailureResponse(message='Invalid username or password',
                                status_code=BAD_REQUEST_CODE).return_response_object()


#Check Seller
@decorator_.rest_api_call(allowed_method_list=['POST'])
def check_seller_record(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

    email_ = data['email'].lower().strip()
    password_ = data['password']
    role_ = data['role'].upper().strip()

    if not Role.objects.filter(name=role_).exists() or role_.upper().strip() != "SELLER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()
    
    user = authenticate(username=email_, password=password_)
    if user:
        return SuccessResponse(message='Password Matched').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='Password does not matched').return_response_object()


#Seller Registration
@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_seller(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

    email_ = data['email'].lower().strip()
    password_ = data['password']
    role_ = data['role'].upper().strip()
    shop_name_ = data['shop_name']
    phone_ = data['phone']
    address_ = data['address']

    #362 24/7 Always open in whole year
    is_always_open_ = data['is_always_open']
    #open and close time for whole week
    open_time_ = data['open_time']
    close_time_ = data['close_time']


    if not Role.objects.filter(name=role_).exists() or role_.upper().strip() != "SELLER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()

    if User.objects.filter(email__iexact=email_).exists():
        userObj = User.objects.get(email=email_)
        if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='This email already exists').return_response_object()
    
    if UserProfile.objects.filter(phone_number=phone_,is_seller=True,).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This phone number already exists').return_response_object()

    if User.objects.filter(email__iexact=email_).exists():
        user = authenticate(username=email_, password=password_)
        if user:
            userObj_ = User.objects.get(email=email_)
            userProfileObj_=UserProfile.objects.get(user=userObj_)
            userProfileObj_.is_seller=True
            userProfileObj_.phone_number = phone_
            userProfileObj_.save()

            roleObj_ = UserRole.objects.create(user=userObj_, role=Role.objects.get(name=role_))
            sellerObj_=Seller.objects.create(user=userObj_, profile=userProfileObj_, role=roleObj_)
            Shop.objects.create(shop_address=address_,shop_name=shop_name_,is_always_open=is_always_open_,open_time=open_time_, close_time = close_time_, seller=sellerObj_)
        else:
            return FailureResponse(message='Invalid Password of previous selected role',
                                status_code=BAD_REQUEST_CODE).return_response_object()
    else:
        user_ = User.objects.create(email=email_, username=email_, first_name=shop_name_)
        user_.set_password(password_)
        user_.save()
        profileObj_ = UserProfile.objects.create(name=shop_name_, user=user_, phone_number = phone_,address=address_, is_seller=True)
        roleObj_ = UserRole.objects.create(user=user_, role=Role.objects.get(name=role_))
        sellerObj_=Seller.objects.create(user=user_, profile=profileObj_, role=roleObj_)
        Shop.objects.create(is_always_open=is_always_open_,open_time=open_time_, close_time = close_time_, seller=sellerObj_)
    user = authenticate(username=email_, password=password_)
    if user:
        token = jwt_.create_user_session(user)
        return SuccessResponse(data={'token': token}).return_response_object()

    else:
        return FailureResponse(message='Invalid username or password',
                                status_code=BAD_REQUEST_CODE).return_response_object()

#Check Driver
@decorator_.rest_api_call(allowed_method_list=['POST'])
def check_driver_record(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

    email_ = data['email'].lower().strip()
    password_ = data['password']
    role_ = data['role'].upper().strip()

    if not Role.objects.filter(name=role_).exists() or role_.upper().strip() != "DRIVER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()
    
    user = authenticate(username=email_, password=password_)
    if user:
        return SuccessResponse(message='Password Matched').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='Password does not matched').return_response_object()
    
    

#Driver Registration
@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_driver(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

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

    name_of_card = data['name_of_card']
    card_number = data['card_number']
    expiry_date = data['expiry_date']
    cvv_number = data['cvv_number']
    billing_address = data['billing_address']
    is_save =data['is_save']


    if not Role.objects.filter(name=role_).exists() or role_.upper().strip() != "DRIVER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()

    if User.objects.filter(email__iexact=email_).exists():
        userObj = User.objects.get(email=email_)
        if UserProfile.objects.filter(is_driver=True, user=userObj).exists():
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='This email already exists').return_response_object()
    
    if UserProfile.objects.filter(phone_number=phone_, is_driver=True).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This phone already exists').return_response_object()
    
    if Driver.objects.filter(social_security_number=social_security_number_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This social security number already exists').return_response_object()
    
    if Vehicle.objects.filter(vehicle_number__iexact=vehicle_number_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This vehicle number already exists').return_response_object()
    
    if License.objects.filter(license_number=license_number_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This License number already exists').return_response_object()
    

    if User.objects.filter(email__iexact=email_).exists():
        user = authenticate(username=email_, password=password_)
        if user:
            userObj_ = User.objects.get(email__iexact=email_)
            userProfileObj_=UserProfile.objects.get(user=userObj_)
            userProfileObj_.is_driver=True
            userProfileObj_.name=name_
            userProfileObj_.phone_number = phone_
            userProfileObj_.address=address_
            userProfileObj_.save()
            roleObj_ = UserRole.objects.create(user=userObj_, role=Role.objects.get(name=role_))
            driverObj = Driver.objects.create(social_security_number=social_security_number_, user=userObj_, profile=userProfileObj_, role=roleObj_)
            License.objects.create(driver=driverObj, license_state=license_state_, license_number=license_number_, license_exp_date=license_exp_date_)
            Vehicle.objects.create(driver=driverObj, vehicle_type=vehicle_type_, vehicle_make=vehicle_make_, vehicle_number=vehicle_number_, vehicle_color=vehicle_color_)
            Bank_card_detail.objects.create(name_of_card=name_of_card,card_number=card_number, expiry_date=expiry_date, cvv_number=cvv_number, billing_address=billing_address, is_save=is_save, driver=driverObj)
        else:
            return FailureResponse(message='Invalid Password of previous selected role',
                                status_code=BAD_REQUEST_CODE).return_response_object()
    else:
        userObj = User.objects.create(email=email_, username=email_, first_name=name_)
        userObj.set_password(password_)
        userObj.save()
        profileObj_ = UserProfile.objects.create(name=name_, user=userObj, date_of_birth=dob_, phone_number = phone_,address=address_, is_driver=True)
        roleObj_ = UserRole.objects.create(user=userObj, role=Role.objects.get(name=role_))
        driverObj = Driver.objects.create(social_security_number=social_security_number_, user=userObj, profile=profileObj_, role=roleObj_)
        License.objects.create(driver=driverObj, license_state=license_state_, license_number=license_number_, license_exp_date=license_exp_date_)
        Vehicle.objects.create(driver=driverObj, vehicle_type=vehicle_type_, vehicle_make=vehicle_make_, vehicle_number=vehicle_number_, vehicle_color=vehicle_color_)
        Bank_card_detail.objects.create(name_of_card=name_of_card,card_number=card_number, expiry_date=expiry_date, cvv_number=cvv_number, billing_address=billing_address, is_save=is_save, driver=driverObj)

    #Directly login
    user = authenticate(username=email_, password=password_)
    if user:
        token = jwt_.create_user_session(user)
        return SuccessResponse(data={'token': token}).return_response_object()
    return FailureResponse(status_code=BAD_REQUEST_CODE, message='Invalid username or password').return_response_object()


#Buyer Registration
@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_buyer(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

    email = data['email'].lower().strip()
    role = data['role'].upper().strip()
    address = data['address']
    password = data['password']

    if not Role.objects.filter(name=role).exists() or role.upper().strip() != "BUYER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()
    
    if User.objects.filter(email__iexact=email).exists():
        userObj = User.objects.get(email=email)
        if UserProfile.objects.filter(is_buyer=True, user=userObj).exists():
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='This user already exists').return_response_object()

    if User.objects.filter(email__iexact=email).exists():
        user = authenticate(username=email, password=password)
        if user:
            userObj_ = User.objects.get(email=email)
            userProfileObj_=UserProfile.objects.get(user=userObj_)
            userProfileObj_.is_buyer=True
            userProfileObj_.save()
        else:
            return FailureResponse(message='Invalid Password of previous selected role',
                                status_code=BAD_REQUEST_CODE).return_response_object()
    else:
        user_ = User.objects.create(email=email, username=email)
        user_.set_password(password)
        user_.save()
        UserProfile.objects.create(user=user_, address=address, is_buyer=True)
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
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

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
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

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
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST

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



#----------------------------------------------Future Work----------------------------

#Seller Shop hours for each day time

  #open and close shops duration per week
    # monday_is_24hours_ = data['monday_is_24hours']
    # monday_open_time_ = data['monday_open_time']
    # monday_close_time_ = data['monday_close_time']

    # tuesday_is_24hours_ = data['tuesday_is_24hours']
    # tuesday_open_time_ = data['tuesday_open_time']
    # tuesday_close_time_ = data['tuesday_close_time']

    # wednesday_is_24hours_ = data['wednesday_is_24hours']
    # wednesday_open_time_ = data['wednesday_open_time']
    # wednesday_close_time_ = data['wednesday_close_time']

    # thursday_is_24hours_ = data['thursday_is_24hours']
    # thursday_open_time_ = data['thursday_open_time']
    # thursday_close_time_ = data['thursday_close_time']

    # friday_is_24hours_ = data['friday_is_24hours']
    # friday_open_time_ = data['friday_open_time']
    # friday_close_time_ = data['friday_close_time']

    # saturday_is_24hours_ = data['saturday_is_24hours']
    # saturday_open_time_ = data['saturday_open_time']
    # saturday_close_time_ = data['saturday_close_time']

    # sunday_is_24hours_ = data['sunday_is_24hours']
    # sunday_open_time_ = data['sunday_open_time']
    # sunday_close_time_ = data['sunday_close_time']

    # shopHourObj = ShopHour.objects.create(is_always_open=is_always_open_, week=
    #                                                     {
    #                                                     'days':[
    #                                                             {
    #                                                                 'name':'monday',
    #                                                                 'is_24hours':monday_is_24hours_,
    #                                                                 'open_time':monday_open_time_,
    #                                                                 'close_time':monday_close_time_, 
    #                                                             },
    #                                                             {
    #                                                                 'name':'tuesday',
    #                                                                 'is_24hours':tuesday_is_24hours_,
    #                                                                 'open_time':tuesday_open_time_,
    #                                                                 'close_time':tuesday_close_time_, 
    #                                                             },
    #                                                             {
    #                                                                 'name':'wednesday',
    #                                                                 'is_24hours':wednesday_is_24hours_,
    #                                                                 'open_time':wednesday_open_time_,
    #                                                                 'close_time':wednesday_close_time_, 
    #                                                             },
    #                                                             {
    #                                                                 'name':'thursday',
    #                                                                 'is_24hours':thursday_is_24hours_,
    #                                                                 'open_time':thursday_open_time_,
    #                                                                 'close_time':thursday_close_time_, 
    #                                                             },
    #                                                             {
    #                                                                 'name':'friday',
    #                                                                 'is_24hours':friday_is_24hours_,
    #                                                                 'open_time':friday_open_time_,
    #                                                                 'close_time':friday_close_time_, 
    #                                                             },
    #                                                             {
    #                                                                 'name':'saturday',
    #                                                                 'is_24hours':saturday_is_24hours_,
    #                                                                 'open_time':saturday_open_time_,
    #                                                                 'close_time':saturday_close_time_, 
    #                                                             },
    #                                                             {
    #                                                                 'name':'sunday',
    #                                                                 'is_24hours':sunday_is_24hours_,
    #                                                                 'open_time':sunday_open_time_,
    #                                                                 'close_time':sunday_close_time_, 
    #                                                             },
    #                                                             ]
    #                                                     }
    # )