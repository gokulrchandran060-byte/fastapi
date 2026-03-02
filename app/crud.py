from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas


class DuplicateEmailError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def create_user(db: Session, user: schemas.UserCreate):
    email = user.email.lower()
    # Quick check before insert for a cleaner API message.
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        raise DuplicateEmailError("Email already registered")

    new_user = models.User(name=user.name.strip(), email=email)
    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError("Email already registered")

    db.refresh(new_user)
    return new_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    # Basic pagination using skip + limit.
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise UserNotFoundError("User not found")
    return db_user


def update_user(db: Session, user_id: int, updated_user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise UserNotFoundError("User not found")

    email = updated_user.email.lower()
    # Prevent using another user's email.
    email_user = db.query(models.User).filter(models.User.email == email).first()
    if email_user and email_user.id != user_id:
        raise DuplicateEmailError("Email already registered")

    db_user.name = updated_user.name.strip()
    db_user.email = email

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError("Email already registered")

    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise UserNotFoundError("User not found")

    db.delete(db_user)
    db.commit()
