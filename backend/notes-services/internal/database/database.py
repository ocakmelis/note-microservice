# Kullanıcılar
#users_db = []
#user_id_counter = 1

# Notlar
#notes_db = []
#note_id_counter = 1

#def get_next_user_id():
#    global user_id_counter
#    current_id = user_id_counter
#    user_id_counter += 1
#    return current_id

#def get_next_note_id():
#    global note_id_counter
#    current_id = note_id_counter
#    note_id_counter += 1
#    return current_id

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./notes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
