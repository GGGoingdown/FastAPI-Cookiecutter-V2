from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    user_id: str = Field(..., alias="sub", description="Mapping to JWT")
    login_at: int = Field(..., alias="iat")

    class Config:
        schema_extra = {
            "example": {
                "sub": "user_id",
                "login_at": 1619446742,
            }
        }


class CreateUser(BaseModel):
    username: str = Field(..., max_length=50)
    email: str = Field(..., max_length=50)
    password: str = Field(..., max_length=128)

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@gmail.com",
                "password": "admin",
            }
        }


class UserInDB(BaseModel):
    id: int
    name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=50, description="Unique")
    password_hash: str = Field(..., max_length=128)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "admin",
                "email": "admin@gmail.com",
                "password_hash": "somehashpassword",
            }
        }
