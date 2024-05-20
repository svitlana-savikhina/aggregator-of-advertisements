from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from database import SessionLocal

pwd_hasher = PasswordHasher()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
