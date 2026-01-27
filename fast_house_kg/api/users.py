from fast_house_kg.database.schema import UserProfileInputSchema, UserProfileOutSchema
from fast_house_kg.database.models import UserProfile
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from fast_house_kg.database.db import SessionLocal

users_router = APIRouter(prefix='/users')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post('/', response_model=UserProfileOutSchema, tags=['Users'], summary='Create user')
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@users_router.get('/', response_model=List[UserProfileOutSchema], summary='Get all users', tags=['Users'])
async def users_list(db: Session = Depends(get_db)):
    users_db = db.query(UserProfile).all()
    if not users_db:
        raise HTTPException(detail='No users.', status_code=404)
    return users_db

@users_router.get('/{user_id}/', response_model=UserProfileOutSchema, summary='Get user by id.', tags=['Users'])
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db1 = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db1:
        raise HTTPException(detail='No user by this id.', status_code=404)
    return user_db1

@users_router.put('/{user_id}/', response_model=dict, summary='Change user.', tags=['Users'])
async def user_update(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db2 = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db2:
        raise HTTPException(detail='No user by this id.', status_code=404)
    for key, value in user.model_dump().items():
        setattr(user_db2, key, value)
    db.commit()
    db.refresh(user_db2)
    return {'detail': 'User has been changed.'}

@users_router.delete('/{user_id}/', response_model=dict, summary='Delete user.', tags=['Users'])
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    user_db3 = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db3:
        raise HTTPException(detail='No user by this id.', status_code=404)
    db.delete(user_db3)
    db.commit()
    return {'detail': 'User has been deleted.'}