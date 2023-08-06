from datetime import datetime, timezone, timedelta
from requests import post as requests_post, codes as requests_status_codes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from json import dumps as json_dumps
from base64 import b64encode
from bc_time.system.encryption.crypt import Crypt
from bc_time.system.constants.encryption.crypt import Crypt as CryptConstants
from bc_time.requests.base import Base as RequestsBase
from bc_time.oauth2.constants.grant_type import GrantType as OAuth2GrantType
from bc_time.api.constants.api import Api as ApiConstants
from bc_time.system.constants.datetime.format import Format as DateTimeFormat

class Token(RequestsBase):
    # Private
    __crypt = None

    # Public
    client_id = None
    client_secret = None
    crypt_key = None
    grant_type = None
    code = None
    private_key_file_path = None
    token = None
    token_expire_as_str = None # This will be stored in UTC.

    @property
    def crypt(self) -> Crypt:
        if self.__crypt is None:
            self.__crypt = Crypt(key=self.crypt_key)
        return self.__crypt

    @crypt.setter
    def crypt(self, value: Crypt):
        self.__crypt = value

    def __init__(self, client_id: str=None, client_secret: str=None, crypt_key: str=None, grant_type: str=None, code: str=None, private_key_file_path: str=None) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.crypt_key = crypt_key
        self.grant_type = grant_type
        self.code = code
        self.private_key_file_path = private_key_file_path

    def request_token(self) -> tuple[bool, dict]:
        if self.__has_valid_token():
            return True, None
        if not self.__validate_data():
            return False, None
        data = self.__get_data()
        if data is None:
            return False, None
        request_response = requests_post(
            url=ApiConstants.OAUTH2_TOKEN_URL,
            data=data
        )
        if request_response.status_code != requests_status_codes.ok:
            return False, None
        response_data = self._get_response_data(request_response.text)
        if not set(('access_token', 'expires_in')).issubset(response_data.keys()):
            return False, response_data
        self.token = response_data['access_token']
        token_expire = datetime.now(timezone.utc) + timedelta(seconds=response_data['expires_in'])
        self.token_expire_as_str = token_expire.strftime(DateTimeFormat.MY_SQL_DATE_TIME)
        return True, response_data

    def __has_valid_token(self) -> bool:
        if self.token is None or self.token_expire_as_str is None:
            return False
        now = datetime.now(timezone.utc)
        return self.token_expire_as_str > now.strftime(DateTimeFormat.MY_SQL_DATE_TIME)

    def __validate_data(self) -> bool:
        if self.grant_type == OAuth2GrantType.AUTH_CODE:
            return self.client_id is not None and self.client_secret is not None and self.code is not None
        elif self.grant_type == OAuth2GrantType.CLIENT_CREDENTIALS:
            return self.client_id is not None and self.client_secret is not None
        elif self.grant_type == OAuth2GrantType.JWT_BEARER:
            return self.client_id is not None and self.private_key_file_path is not None
        return False

    def __get_data(self) -> dict:
        if self.grant_type == OAuth2GrantType.AUTH_CODE:
            return {
                'grant_type': self.grant_type,
                'client_id': self.client_id,
                'client_secret': self.__get_client_secret(),
                'code': self.code,
            }
        elif self.grant_type == OAuth2GrantType.CLIENT_CREDENTIALS:
            return {
                'grant_type': self.grant_type,
                'client_id': self.client_id,
                'client_secret': self.__get_client_secret(),
            }
        elif self.grant_type == OAuth2GrantType.JWT_BEARER:
            return {
                'grant_type': self.grant_type,
                'assertion': self.__get_jwt_assertion(),
            }

    def __get_client_secret(self) -> str:
        if self.crypt_key is not None:
            self.crypt.data = self.client_secret
            return self.crypt.encrypt()
        return self.client_secret

    def __get_jwt_assertion(self, separator: str='.') -> list:
        assertion_data = self.__get_jwt_assertion_data()
        assertion_data.append(self.__get_jwt_assertion_data_signature(
            assertion_data=assertion_data,
            separator=separator
        ))
        return separator.join(assertion_data)

    def __get_jwt_assertion_data(self, expire_in_seconds: int=60) -> list:
        expire_datetime = datetime.now(timezone.utc) + timedelta(seconds=expire_in_seconds)
        assertion_data = [
            {'algo': CryptConstants.PHP_OPENSSL_ALGO_SHA1},
            {
                'client_id': self.client_id,
                'issued': datetime.now(timezone.utc).strftime(DateTimeFormat.MY_SQL_DATE_TIME),
                'expire': expire_datetime.strftime(DateTimeFormat.MY_SQL_DATE_TIME),
            },
        ]
        return list(map(lambda data_value: str(b64encode(bytes(json_dumps(data_value), 'utf8')), 'utf8'), assertion_data))

    def __get_jwt_assertion_data_signature(self, assertion_data: list, separator: str) -> str:
        with open(self.private_key_file_path, mode='rb') as opened_key_file:
            private_key = serialization.load_pem_private_key(
                opened_key_file.read(),
                password=None
            )
        sign_data = separator.join(assertion_data)
        signature = private_key.sign(
            data=bytes(sign_data, 'utf8'),
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA1()
        )
        return str(b64encode(signature), 'utf8')