from datetime import datetime, timezone
from time import time
import jwt
from functools import wraps

class ApoJWT():
    """A standard access/refresh JWT implementation that provides convenient decorators and functions
    
    Keyword Arguments (those with asterisks are functions):

    JWT Validation
        secret: Secret string used to encode and decode the access JWT
        exp_period: Length of time in seconds access tokens should be valid for. Default 900 (15 minutes) 
        iss: Issuer string used for additional security. Default ""
        server_audience: Audience name of the server hosting the HTTP framework. 
            Audience names are typically base address URLs. Ex: https://example.com
        algorithm: The algorithm to use when encoding/decoding. Default HS256
        * token_finder: Function used to retrieve the access JWT from http request Authorization header. Default None

    Framework Configuration
        asynch: Tells ApoJWT to use async decorators instead of the normal (FastAPI needs this True). Default False
        * exception_handler: HTTP error handling function given an HTTP code and message as arguments

    Utility
        * permission_formatter: String formatting function that is given permission_name as an argument
            Can be used to format request data in the permission name
    """

    def __init__(self, secret: str, exp_period: int=900, iss: str="", asynch: bool=False, server_audience: str="default", algorithm: str="HS256", token_finder=None, permission_formatter=None, exception_handler=None):        
        self.exp_period = int(exp_period)
        self.refresh_exp_period = 0
        self.iss = str(iss)
        self.asynch = asynch
        self.algorithm = algorithm

        self.__token_f = token_finder
        self.__permission_formatter = permission_formatter
        self.__exception_handler = exception_handler
        self.__secret = str(secret)
        self.__server_aud = server_audience
        self.__refresh_flag = False
        self.__refresh_f = None
        self.__refresh_secret = None


    def config_refresh(self, refresh_secret: str, refresh_exp_period: int=86400, refresh_finder=None):
        """Configures ApoJWT for use with refresh tokens

        refresh_secret: Secret string used to encode and decode the refresh JWT
        refresh_finder: Function used to retrieve the refresh JWT from an http-only cookie. Default None
        refresh_exp_period: Number of seconds for the refresh token to be valid. Default 86400 (1 day)
        """

        self.__refresh_flag = True
        self.__refresh_f = refresh_finder
        self.__refresh_secret = refresh_secret
        self.refresh_exp_period = refresh_exp_period


    def token_required(self, fn):
        """Verifies a JWT and all its claims
        
        auth_header: http "Authorization" request header (contains the JWT)

        Raises an exception if any claims are invalid
            - expired token
            - invalid secret
            - invalid issuer
        """
        if self.asynch is True:
            @wraps(fn)
            async def wrapper(*args, **kwargs):
                if self.__token_f is None:
                    raise TypeError("ApoJWT requires the token_finder attribute to be defined for validating JWTs")
                token = self.__token_f(*args, **kwargs)
                token_dict = self.__decode(token, *args, **kwargs)
                return await fn(token_data=token_dict["data"], token_subject=token_dict["sub"], *args, **kwargs)
            return wrapper
        else:
            @wraps(fn)
            def wrapper(*args, **kwargs):
                if self.__token_f is None:
                    raise TypeError("ApoJWT requires the token_finder attribute to be defined for validating JWTs")
                token = self.__token_f(*args, **kwargs)
                token_dict = self.__decode(token, *args, **kwargs)
                return fn(token_data=token_dict["data"], token_subject=token_dict["sub"], *args, **kwargs)
            return wrapper
        

    def permission_required(self, permission: str):
        """Verifies a JWT and ensures it contains the correct permission for the resource
    
        permission: permission string that will be fed into permission_formatter if defined

        Raises an exception if any claims are invalid
            - expired token
            - invalid secret
            - invalid issuer
            - invalid audience
        """
        def permission_decorated(fn):
            if self.asynch is True:
                @wraps(fn)
                async def wrapper(*args, **kwargs):
                    if self.__token_f is None:
                        raise TypeError("ApoJWT requires the token_finder attribute to be defined for validating JWTs")
                    token = self.__token_f(*args, **kwargs)
                    token_dict = self.__decode(token, *args, **kwargs)
                    decoded_permissions = token_dict["perms"]
                    formatted_perm = permission if self.__permission_formatter is None else self.__permission_formatter(permission=permission, *args, **kwargs)
                    if formatted_perm not in decoded_permissions:
                        if self.__exception_handler is None:
                            raise jwt.exceptions.InvalidTokenError(f"403: JWT is not authorized for this action")
                        else:
                            self.__exception_handler(code=403, exception_type="unauthorized", msg="JWT is not authorized for this action", *args, **kwargs)
                            raise NotImplementedError("ApoJWT Exception Handler must not return control")
                    return fn(token_data=token_dict["data"], token_subject=token_dict["sub"], *args, **kwargs)
                return wrapper
            else: 
                @wraps(fn)
                def wrapper(*args, **kwargs):
                    if self.__token_f is None:
                        raise TypeError("ApoJWT requires the token_finder attribute to be defined for validating JWTs")
                    token = self.__token_f(*args, **kwargs)
                    token_dict = self.__decode(token, *args, **kwargs)
                    decoded_permissions = token_dict["perms"]
                    formatted_perm = permission if self.__permission_formatter is None else self.__permission_formatter(permission, *args, **kwargs)
                    if formatted_perm not in decoded_permissions:
                        if self.__exception_handler is None:
                            raise jwt.exceptions.InvalidTokenError(f"403: JWT is not authorized for this action")
                        else:
                            self.__exception_handler(code=403, exception_type="unauthorized", msg="JWT is not authorized for this action", *args, **kwargs)
                            raise NotImplementedError("ApoJWT Exception Handler must not return control")
                    return fn(token_data=token_dict["data"], token_subject=token_dict["sub"], *args, **kwargs)
                return wrapper
        return permission_decorated


    def refresh(self, fn):
        """Verifies a refresh token and returns a new access token"""
        if self.asynch is True:
            @wraps(fn)
            async def wrapper(*args, **kwargs):
                if self.__token_f is None:
                    raise NotImplementedError("ApoJWT requires the token_finder attribute to be defined for refreshing JWTs")
                if self.__refresh_f is None:
                    raise NotImplementedError("ApoJWT requires the refresh_finder attribute to be defined for refreshing JWTs")
                ref_token = self.__refresh_f(*args, **kwargs)
                jwt.decode(ref_token, self.__refresh_secret, issuer=self.iss, audience="default", algorithms=[self.algorithm])
                acc_token = self.__token_f(*args, **kwargs)
                token_payload = self.__decode(acc_token, verify_exp=False, *args, **kwargs)
                token_payload["exp"] = int(time()) + self.exp_period
                new_token = jwt.encode(token_payload, self.__secret, algorithm=self.algorithm)
                return await fn(access_token=new_token, *args, **kwargs)
            return wrapper
        else:
            @wraps(fn)
            def wrapper(*args, **kwargs):
                if self.__token_f is None:
                    raise NotImplementedError("ApoJWT requires the token_finder attribute to be defined for refreshing JWTs")
                if self.__refresh_f is None:
                    raise NotImplementedError("ApoJWT requires the refresh_finder attribute to be defined for refreshing JWTs")
                ref_token = self.__refresh_f(*args, **kwargs)
                self.__decode(ref_token, secret=self.__refresh_secret, *args, **kwargs)
                acc_token = self.__token_f(*args, **kwargs)
                token_payload = self.__decode(acc_token, verify_exp=False, *args, **kwargs)
                token_payload["exp"] = int(time()) + self.exp_period
                new_token = jwt.encode(token_payload, self.__secret, algorithm=self.algorithm)
                return fn(access_token=new_token, *args, **kwargs)
            return wrapper
        

    def create_token(self, sub: str="", permissions: list[str]=[], aud: list[str]=[], data: dict=dict(), refresh_data: dict=dict()):
        """Encodes and returns an access JWT and optionally a refresh JWT

        sub: Subject of the JWT (typically some reference to the user of JWT)
        permissions: List of permissions to assign to token
        aud: List of audiences token should be accepted by
        data: Any additional information that is needed
        refresh: Flag to include a refresh token as a second return value
        refresh_data: If refresh is True, this additional data is stored with the refresh token

        JWT will contain the following claims:
            - exp: Expiration Time
            - nbf: Not Before Time
            - iss: Issuer
            - aud: Audience
            - iat: Issued At
        """
        exp = int(time()) + self.exp_period
        aud.append(self.__server_aud)
        payload = {
            "exp": int(exp),
            "sub": str(sub),
            "nbf": datetime.now(tz=timezone.utc),
            "iss": self.iss,
            "aud": list(aud),
            "iat": datetime.now(tz=timezone.utc),
            "data": data,
            "perms": list(permissions)
        }
        access_token = jwt.encode(payload, self.__secret, algorithm=self.algorithm)
        if self.__refresh_flag is True:
            if self.__refresh_secret is None:
                raise ValueError("The refresh secret must be assigned using config_refresh")
            ref_exp = int(time()) + self.refresh_exp_period
            refresh_payload = {
                "exp": ref_exp,
                "nbf": datetime.now(tz=timezone.utc),
                "iss": self.iss,
                "aud": list(aud),
                "iat": datetime.now(tz=timezone.utc),
                "data": refresh_data
            }
            refresh_token = jwt.encode(refresh_payload, self.__refresh_secret, algorithm=self.algorithm)
            return access_token, refresh_token
        return access_token





    def __decode(self, token, secret=None, verify_exp=True, *args, **kwargs):
        """Decodes the active jwt and returns the result"""
        not_implemented = NotImplementedError("ApoJWT Exception Handler must not return control")
        if secret is None:
            secret = self.__secret
        try:
            decoded = jwt.decode(token, secret, issuer=self.iss, audience=self.__server_aud, algorithms=[self.algorithm], options={'verify_exp': verify_exp})
            return decoded
        except jwt.exceptions.InvalidSignatureError:
            if self.__exception_handler is None:
                raise jwt.exceptions.InvalidSignatureError(f"401: JWT signature is invalid")
            else:
                self.__exception_handler(code=401, exception_type="signature", msg="JWT signature is invalid", *args, **kwargs)
                raise not_implemented
        except jwt.exceptions.ExpiredSignatureError:
            if self.__exception_handler is None:
                raise jwt.exceptions.ExpiredSignatureError(f"403: JWT signature has expired")
            else:
                self.__exception_handler(code=403, exception_type="expired", msg="JWT signature has expired", *args, **kwargs)
                raise not_implemented
        except jwt.exceptions.InvalidIssuerError:
            if self.__exception_handler is None:
                raise jwt.exceptions.InvalidIssuerError(f"401: JWT issuer is invalid")
            else:
                self.__exception_handler(code=401, exception_type="issuer", msg="JWT issuer is invalid", *args, **kwargs)
                raise not_implemented
        except jwt.exceptions.InvalidAudienceError:
            if self.__exception_handler is None:
                raise jwt.exceptions.InvalidAudienceError(f"401: JWT audience is invalid")
            else:
                self.__exception_handler(code=401, exception_type="audience", msg="JWT audience is invalid", *args, **kwargs)
                raise not_implemented
        except jwt.exceptions.InvalidTokenError:
            if self.__exception_handler is None:
                raise jwt.exceptions.InvalidTokenError(f"401: JWT is invalid")
            else:
                self.__exception_handler(code=401, exception_type="invalid", msg="JWT is invalid", *args, **kwargs)
                raise not_implemented
