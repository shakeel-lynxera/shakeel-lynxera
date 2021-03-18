from os import name
from utilities.models import Temp_Product_Barcode_Scanner
from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from .models import *
from django.contrib.auth import authenticate
from utilities.jwt import JWTClass

decorator_ = DecoratorHandler()
jwt_ = JWTClass()


#Add Vendor
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
    shop_id_ = data['shop_id']

    if role_.upper().strip() != "VENDOR":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User role is not valid").return_response_object()
    
    if Vendor.objects.filter(email_address=email_address_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User email already exists").return_response_object()
    
    if Vendor.objects.filter(phone_number=phone_number_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User phone number already exists").return_response_object()
    else:
        if Shop.objects.filter(id=shop_id_).exists():
            shopObj = Shop.objects.get(id=shop_id_)
            Vendor.objects.create(full_name=full_name_, email_address=email_address_, phone_number=phone_number_, company=company_, shop=shopObj)
            return SuccessResponse(message='Vendor Created Successfully').return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message="Shop does not exists").return_response_object()


#Show Vendor
@decorator_.rest_api_call(allowed_method_list=['POST'])
def show_vendor(request):
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
    
    token_ = data['token']
    shop_id_ = data['shop_id']

    jwtDecodeObject = jwt_.decode_jwt_token(token_)
    email_ = jwtDecodeObject['email']
    role_ = jwtDecodeObject['role']

    if role_.upper().strip() != "SELLER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User role is not valid").return_response_object()

    if User.objects.filter(email__iexact=email_).exists():
        userObj = User.objects.get(email=email_)
        if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
            sellerObj = Seller.objects.get(user=userObj)
            if Shop.objects.filter(id=shop_id_, seller=sellerObj).exists():
                shopsObject = Shop.objects.get(id=shop_id_)
                venderObjects = Vendor.objects.filter(shop=shopsObject)
                vendors = []
                for obj in venderObjects:
                    dict_ = {'id': obj.id, 'vendor name': obj.full_name, 'phone_number':obj.phone_number, 'email':obj.email_address, 'company':obj.company}
                    vendors.append(dict_)
                return SuccessResponse(data={'vendors': vendors}).return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message="Shop does not belong to the requested seller").return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message="Seller role is not active").return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User does not exists").return_response_object()


#Get shops for current seller
@decorator_.rest_api_call(allowed_method_list=['POST'])
def get_shop_seller_detais(request):
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
    
    token_ = data['token']

    jwtDecodeObject = jwt_.decode_jwt_token(token_)
    email_ = jwtDecodeObject['email']
    role_ = jwtDecodeObject['role']

    if role_.upper().strip() != "SELLER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User role is not valid").return_response_object()

    if User.objects.filter(email__iexact=email_).exists():
        userObj = User.objects.get(email=email_)
        if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
            sellerObj = Seller.objects.get(user=userObj)
            shopsObjects = Shop.objects.filter(seller=sellerObj)

            shops = []
            for obj in shopsObjects:
                dict_ = {'id': obj.id, 'shop name': obj.shop_name, 'shop address': obj.shop_address}
                shops.append(dict_)

            return SuccessResponse(data={'shops': shops}).return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='Seller role not active').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This user does not exists').return_response_object()


#Get the current login seller and shop details and also get the product category and type details
@decorator_.rest_api_call(allowed_method_list=['POST'])
def get_shop_seller_vendor_product_detais_for_add_product(request):
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
    
    token_ = data['token']
    shop_id_ = data['shop_id']

    jwtDecodeObject = jwt_.decode_jwt_token(token_)
    email_ = jwtDecodeObject['email']
    role_ = jwtDecodeObject['role']

    if role_.upper().strip() != "SELLER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User role is not valid").return_response_object()

    if User.objects.filter(email__iexact=email_).exists():
        userObj = User.objects.get(email=email_)
        if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
            sellerObj = Seller.objects.get(user=userObj)
            if Shop.objects.filter(id=shop_id_, seller=sellerObj).exists():
                shopsObject = Shop.objects.get(id=shop_id_)
                venderObjects = Vendor.objects.filter(shop=shopsObject)
                vendors = []
                for obj in venderObjects:
                    dict_ = {'id': obj.id, 'vendor name': obj.full_name}
                    vendors.append(dict_)
                
                getAllProducts = Temp_Product_Barcode_Scanner.objects.all()
                products = []
                for productObj in getAllProducts:
                    product_dict_ = {'product_category':productObj.category, 'product_type':productObj.type}
                    products.append(product_dict_)

                return SuccessResponse(data={'vendors': vendors, 'products_details':products}).return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message='Shop does not belongs to requested user').return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='Seller role not active').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This user does not exists').return_response_object()