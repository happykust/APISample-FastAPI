from pydantic import BaseModel


class UserCreateUpdateSchema(BaseModel):
    """
    User create/update schema
    """
    username: str
    password: str


class TokenData(BaseModel):
    """
    Token data schema
    """
    username: str | None = None


class Token(BaseModel):
    """
    Token schema
    """
    access_token: str
    token_type: str
