import jwt

from datetime import datetime, timedelta
from django.conf import settings


class TokensPair():
    token_pairs_dict = {}


dict_tokens = TokensPair()


def create_refresh_token(email):
    dt = datetime.now() + timedelta(days=30)
    refresh_token = jwt.encode({
        'email': email,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')
    refresh_token_short = refresh_token.split('.')[2]
    # dict_tokens[email] = {}
    # dict_tokens[email]['refresh_token'] = refresh_token
    return refresh_token_short


def create_access_token(obj):
    dt = datetime.now() + timedelta(seconds=30)
    access_token = jwt.encode({
        'email': obj.email,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')
    # dict_tokens[obj.email]['access_token'] = access_token
    return access_token
