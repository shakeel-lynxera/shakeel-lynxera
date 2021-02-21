import datetime
import json
import uuid
from datetime import timedelta

import jwt

from backend.settings import ConfigFile


class JWTClass:
    def __init__(self):
        self.Path = ConfigFile
        self.TokenProvider = self.get_jwt_information()

    @staticmethod
    def generate_specification():
        return uuid.uuid1()

    @staticmethod
    def get_user_roles(user):
        ur = user.UserRole.all()
        return [{'role_id': x.id, 'name': x.name} for x in ur]

    def get_jwt_information(self):
        config_file = open(self.Path, 'r')
        config_file = json.loads(config_file.read())
        token_provider = config_file['data']['tokenProvider']
        return token_provider

    def get_expiry_date(self):
        date_ = datetime.datetime.now() + timedelta(minutes=int(self.TokenProvider['tokenExpiration']))
        return date_, date_.timestamp()

    def get_jwt_model(self, email, claims, roles, expiry_date, specification):
        return {
            'audience': self.TokenProvider['tokenAudience'],
            'expiry': expiry_date,
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress': email,
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name': claims,
            'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/role': roles,
            'issuer': self.TokenProvider['tokenIssuer'],
            'specification': specification
        }

    def generate_jwt_token(self, email, claims, roles, expiry_date, specification):
        data_ = self.get_jwt_model(email, claims, roles, expiry_date, specification)
        encoded_token = jwt.encode(data_, self.TokenProvider['tokenSecurityKey'],
                                   algorithm=self.TokenProvider['tokenSecurityAlgorithm'])
        encoded_token = encoded_token.decode('utf-8')
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
            UserSession.objects.filter(Specification=decoded_token['specification'],
                                       Expiry=expiry_).update(IsValid=False)
            return True
        except Exception as e:
            return False

    def create_user_session(self, user, user_role_given=None):
        date, timestamp = self.get_expiry_date()
        specification = str(self.generate_specification())

        role_allowed = False
        if not user_role_given:
            user_role_given = user.UserRole.all()
            if user_role_given.count() == 1:
                user_role_given = user_role_given[0].id
                role_allowed = True
        else:
            role_allowed = True
        #
        # if role_allowed:
        #     UserSession.objects.filter(UserId=user, UserRole=user_role_given).update(IsPushValid=False)
        #     UserSession.objects.create(UserId=user, Expiry=date, Specification=specification, UserRole=user_role_given)
        # else:
        #     UserSession.objects.create(UserId=user, Expiry=date, Specification=specification, UserRole=0)
        return self.generate_jwt_token(user.Email, [], self.get_user_roles(user), timestamp, specification)
