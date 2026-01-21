from sqlalchemy.orm import Session
from internal.models.user_model import User # Model yolunun doğruluğunu teyit et

class UserRepository:
    # Sadece veritabanı sorgusu yapar, iş mantığı içermez.
    
    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_username(db: Session, username: str):
        # Username üzerinden kullanıcıyı bulur (Login ve Register kontrolleri için)
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_user(db: Session, user_obj: User):
        # Yeni kullanıcıyı veritabanına yazar
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

    @staticmethod
    def delete_user(db: Session, user_id: int):
        # Kullanıcıyı siler 
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return user