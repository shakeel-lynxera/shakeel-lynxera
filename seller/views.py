from os import name
from utilities.models import Temp_Product_Barcode_Scanner
from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from utilities.utils import get_request_obj
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
    data = get_request_obj(request)

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
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def get_shop_seller_detais(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message="Please fill all the values").return_response_object()

    userObj = request.user

    if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
        sellerObj = Seller.objects.get(user=userObj)
        shopsObjects = Shop.objects.filter(seller=sellerObj)

        shops = []
        for obj in shopsObjects:
            dict_ = {
                'id': obj.id,
                'shop_name': obj.shop_name,
                'shop_address': obj.shop_address,
                'shop_image_link':"https://kwkdrop.s3-us-east-2.amazonaws.com/media/1_LK4H69l.jpg"
            }
            shops.append(dict_)

        return SuccessResponse(data={'shops': shops}).return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='Seller role not active').return_response_object()


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


#Add Product in shop
@decorator_.rest_api_call(allowed_method_list=['POST'])
def Add_Product_in_shop(request):
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
    vendor_id_ = data['vendor_id']
    
    #product attributes
    title_ = data['title']
    description_ = data['description']
    price_ = data['price']
    sale_price_ = data['sale_price']
    is_active_ = data['is_active']
    sku_ = data['sku']
    barcode_ = data['barcode']
    quantity_ = data['quantity']
    weight_ = data['weight']
    weight_unit_ = data['weight_unit']
    tags_ = data['tags']
    variants_ = data['variants']
    product_category_ = data['product_category']
    product_type_ = data['product_type']


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
                if Vendor.objects.filter(id=vendor_id_, shop=shopsObject).exists():
                    vendorObj = Vendor.objects.get(id=vendor_id_)
                    if Shop_Product.objects.filter(barcode=barcode_, shop=shopsObject, seller=sellerObj).exists():
                        return FailureResponse(status_code=BAD_REQUEST_CODE, message="Product Barcode already exist").return_response_object()

                    if Shop_Product.objects.filter(sku=sku_, shop=shopsObject, seller=sellerObj).exists():
                        return FailureResponse(status_code=BAD_REQUEST_CODE, message="Product SKU already exist").return_response_object()
                    productObj = Shop_Product.objects.create(
                                                                title = title_,
                                                                description = description_,
                                                                price = price_,
                                                                sale_price = sale_price_,
                                                                is_active = is_active_,
                                                                sku = sku_,
                                                                barcode = barcode_,
                                                                quantity = quantity_,
                                                                weight = weight_,
                                                                weight_unit = weight_unit_,
                                                                tags = tags_,
                                                                vendor = vendorObj,
                                                                shop = shopsObject,
                                                                seller = sellerObj
                                )
                    categoryObj = Shop_Product_Category.objects.create(name=product_category_, shop_product=productObj)
                    Shop_Product_Type.objects.create(name=product_type_, shop_product_category = categoryObj)
                    
                    for i in range(len(variants_)):
                        variant_name = variants_[i]['variant_name']
                        variant_value = variants_[i]['variant_value']
                        variant_price = variants_[i]['variant_price']
                        variant_sale_price = variants_[i]['variant_sale_price']
                        variant_sku = variants_[i]['variant_sku']
                        variant_barcode = variants_[i]['variant_barcode']
                        variant_quantity = variants_[i]['variant_quantity']

                        Shop_Product_Variant.objects.create(
                            name = variant_name,
                            value = variant_value,
                            price = variant_price,
                            sale_price = variant_sale_price,
                            sku = variant_sku,
                            barcode = variant_barcode,
                            quantity = variant_quantity,
                            shop_product = productObj,
                        )
                    return SuccessResponse(message='Product Created Sucessfully').return_response_object()
                else:
                    return FailureResponse(status_code=BAD_REQUEST_CODE, message="invalid vendor for the requested shop").return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message="Shop does not belong to the requested seller").return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message="Seller role is not active").return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="User does not exists").return_response_object()


#Get Products of specific shop of specific seller
@decorator_.rest_api_call(allowed_method_list=['POST'])
def Get_Product_for_shop(request):
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
                
                getAllProducts = Shop_Product.objects.filter(shop=shopsObject)
                products = []
                for productObj in getAllProducts:
                    productCategoryObj = Shop_Product_Category.objects.get(shop_product=productObj)
                    product_dict_ = {
                                        'title':productObj.title,
                                        'price':productObj.price,
                                        'category':productCategoryObj.name,
                                        'is_active':productObj.is_active,
                                        'quantity':productObj.quantity,
                                        'product_image_link':"https://kwkdrop.s3-us-east-2.amazonaws.com/media/1_LK4H69l.jpg"
                                    }
                    products.append(product_dict_)
                return SuccessResponse(data={'products_details':products}).return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message='Shop does not belongs to requested user').return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='Seller role not active').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='This user does not exists').return_response_object()