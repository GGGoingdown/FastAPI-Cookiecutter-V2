from pydantic import BaseModel, Field

# Reference: https://python-jose.readthedocs.io/en/latest/jwt/index.html
class JWTPayload(BaseModel):
    sub: str
    exp: int = Field(..., description="The time after which the token is invalid.")
    iat: int = Field(..., description="The time at which the JWT was issued.")

    class Config:
        schema_extra = {
            "example": {
                "sub": "user_id",
                "exp": 1619446742,
                "iat": 1619446742,
            }
        }
