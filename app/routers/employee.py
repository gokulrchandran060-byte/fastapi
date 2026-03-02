from typing import List

from fastapi import APIRouter, Depends, Path, Query, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(tags=["Users"])


@router.post(
    "/users/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.get(
    "/users/",
    response_model=List[schemas.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    # Keep pagination simple for now.
    return crud.get_users(db=db, skip=skip, limit=limit)


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
)
def read_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_user(db=db, user_id=user_id)


@router.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    updated_user: schemas.UserCreate,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    return crud.update_user(db=db, user_id=user_id, updated_user=updated_user)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    crud.delete_user(db=db, user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
