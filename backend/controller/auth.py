from sqlalchemy.orm import Session
from database import schemas, models
from controller import crud
import jwt
import config
import requests


class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, db: Session, token):
        self.db = db
        self.token = token
        self.config = config.get_settings()

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.config.auth0_domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config.auth0_algorithms,
                audience=self.config.auth0_api_audience.split(','),
                issuer=self.config.auth0_issuer,
            )

            url = ("%suserinfo" % (self.config.auth0_issuer))
            response = requests.post(url, headers={"Authorization": (
                "Bearer %s" % (self.token)), "Content-Type": "application/json"})
            res = response.json()
            user = crud.get_user_by_email(self.db, res['email'])
            if not user:
                u_schema = schemas.UserCreate(first_name=(res['nickname'])[
                                              :50], last_name="", email=res['email'])
                user = crud.create_user(self.db, u_schema)
            return user
        except Exception as e:
            return None
