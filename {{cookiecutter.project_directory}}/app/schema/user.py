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
