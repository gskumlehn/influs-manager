from app.infra.database import get_session
from app.models.user import User

class UserRepository:
    @staticmethod
    def create(user: User) -> User:
        with get_session() as session:
            session.add(user)
            session.flush()
            session.refresh(user)
            return user
    
    @staticmethod
    def find_by_email(email: str):
        with get_session() as session:
            user = session.query(User).filter(User.email == email).first()
            return user
    
    @staticmethod
    def find_by_id(user_id: int):
        with get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            return user
