"""auth 기능의 API DTO."""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    passcode: str


class AuthStatus(BaseModel):
    authenticated: bool
