from app.repositories import CRUDBase
from app.models import User


class UserRepository(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=User)
