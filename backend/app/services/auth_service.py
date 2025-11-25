import os
from datetime import datetime, timedelta

import bcrypt
import jwt

from app.repositories.user_repository import UserRepository

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

class AuthService:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def login(email: str, password: str):
        user = UserRepository.find_by_email(email)
        if not user:
            return None
        if not AuthService.verify_password(password, user["password_hash"]):
            return None
        token = AuthService.create_access_token({"user_id": user["id"], "email": user["email"]})
        return {
            "token": token,
            "user": user
        }
    
    @staticmethod
    def register(email: str, password: str, role: str, company_id: int = None):
        existing_user = UserRepository.find_by_email(email)
        if existing_user:
            return None
        data = {
            "email": email,
            "password_hash": AuthService.hash_password(password),
            "role": role,
            "company_id": company_id
        }
        return UserRepository.create(data)
