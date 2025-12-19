from user_services import create_user, authenticate_user, set_username
from ..models.user_models import UserBase
import math

def create_user_handler(user_data: UserBase):
    user_data=user_services.set_username(user_data)
    return create_user(user_data)

def login_handler(user_data):
    return user_services.login(user_data)