import datetime
import json
import uuid
from datetime import timedelta

import jwt

from kwk.settings import ConfigFile
from django.contrib.auth.models import User
from authModule.models import UserRole


class JWTClass:
    def __init__(self):
        self.Path = ConfigFile
        self.TokenProvider = self.get_jwt_information()

    @staticmethod
    def get_user_roles(user):
        ur = UserRole.objects.filter(user=user)
        return [{'role': x.role.name} for x in ur]

    def get_jwt_information(self):
        config_file = open(self.Path, 'r')
        config_file = json.loads(config_file.read())
        token_provider = config_file['data']['tokenProvider']
        return token_provider

    def get_expiry_date(self):
        date_ = datetime.datetime.now() + timedelta(minutes=int(self.TokenProvider['tokenExpiration']))
        return date_, date_.timestamp()

    def get_jwt_model(self, email, claims, roles, expiry_date):
        return {
            'audience': self.TokenProvider['tokenAudience'],
            'expiry': expiry_date,
            'emailaddress': email,
            'name': claims,
            'role': roles,
            'issuer': self.TokenProvider['tokenIssuer']
        }

    def generate_jwt_token(self, email, claims, roles, expiry_date):
        data_ = self.get_jwt_model(email, claims, roles, expiry_date)
        encoded_token = jwt.encode(data_, self.TokenProvider['tokenSecurityKey'],
                                   algorithm=self.TokenProvider['tokenSecurityAlgorithm'])
        # encoded_token = encoded_token.decode('utf-8')
        return encoded_token

    @staticmethod
    def response_user_id(us_):
        if us_:
            return us_.UserId
        return False

    def decode_jwt_token(self, token, role_check=None):
        try:
            decoded_token = jwt.decode(token, self.TokenProvider['tokenSecurityKey'],
                                       algorithm=[self.TokenProvider['tokenSecurityAlgorithm']])
            expiry_ = datetime.datetime.fromtimestamp(decoded_token['expiry'])

            user_ = User.objects.filter(email__iexact=decoded_token['email']).last()


            # if expiry_ > datetime.datetime.now():
            us_ = UserSession.objects.filter(Specification=decoded_token['specification'], IsValid=True,
                                             Expiry=expiry_).last()
            if role_check:
                if us_.UserRole in role_check:
                    return self.response_user_id(us_)
                elif us_.UserRole == 0:
                    us_.UserRole = role_check[0]
                    us_.save()
                    return self.response_user_id(us_)
            else:
                return self.response_user_id(us_)

            return False
        except Exception as e:
            return False

    def decode_jwt_token_and_logout(self, token):
        try:
            decoded_token = jwt.decode(token, self.TokenProvider['tokenSecurityKey'],
                                       algorithm=[self.TokenProvider['tokenSecurityAlgorithm']])
            expiry_ = datetime.datetime.fromtimestamp(decoded_token['expiry'])
            return True
        except Exception as e:
            return False

    def create_user_session(self, user):
        date, timestamp = self.get_expiry_date()
        return self.generate_jwt_token(user.email, [], self.get_user_roles(user), timestamp)
