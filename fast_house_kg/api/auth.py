from fast_house_kg.database.db import SessionLocal
from fast_house_kg.database.models import UserProfile, UserProfileRefreshToken
from fast_house_kg.database.schema import UserProfileInputSchema, UserProfileLoginSchema
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, APIRouter
from fast_house_kg.config import ALGORITHM, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Optional
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))

@auth_router.post('/register/', response_model=dict, tags=['Auth'])
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    username_db = db.query(UserProfile).filter(UserProfile.username==user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email==user.email).first()
    if username_db:
        raise HTTPException(detail='This username already exists.', status_code=400)
    if email_db:
        raise HTTPException(detail='This email already exists.', status_code=400)
    hashed_password = get_password_hash(user.password)
    user_db = UserProfile(
        username=user.username,
        pasword=hashed_password,
        email=user.email,
        status=user.status
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return {'detail': 'Successfully registered in.'}

@auth_router.post('/login/', response_model=dict, tags=['Auth'])
async def login(user: UserProfileLoginSchema, db: Session = Depends(get_db)):
    username_db1 = db.query(UserProfile).filter(UserProfile.username==user.username).first()
    if not username_db1 or not verify_password(user.password, username_db1.password):
        raise HTTPException(detail='Invalid credentials.', status_code=401)
    access_token = create_access_token({'sub': username_db1.username})
    refresh_token = create_refresh_token({'sub': username_db1.username})
    token_db = UserProfileRefreshToken(
        user_id=username_db1.id,
        token=refresh_token
    )
    db.add(token_db)
    db.commit()
    return {
        'access': access_token,
        'refresh': refresh_token,
        'token_type': 'Bearer'
    }

@auth_router.post('/logout/', tags=['Auth'], response_model=dict)
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    old_token = db.query(UserProfile).filter(UserProfileRefreshToken.token==refresh_token).first()
    if not old_token:
        raise HTTPException(detail='Invalid token.', status_code=401)
    db.delete(old_token)
    db.commit()
    return {'detail': 'Successfully logged out.'}

@auth_router.post('/refresh/', response_model=dict, tags=['Auth'])
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(UserProfile).filter(UserProfileRefreshToken.token==refresh_token).first()
    if not stored_token:
        raise HTTPException(detail='Token already exists.', status_code=402)
    access_token = create_access_token({'sub': stored_token.id})
    return {'access_token': access_token, 'token_type': 'Bearer'}