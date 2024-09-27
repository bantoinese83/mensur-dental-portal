from pydantic import BaseModel
from pydantic.v1 import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordReset(BaseModel):
    token: str
    new_password: str


class MFAVerifyRequest(BaseModel):
    email: EmailStr
    token: str


class MFAEnableRequest(BaseModel):
    email: EmailStr
