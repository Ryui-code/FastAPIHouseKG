from fast_house_kg.database.schema import CityOutSchema, CityInputSchema
from fast_house_kg.database.models import City
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from fast_house_kg.database.db import SessionLocal

city_router = APIRouter(prefix='/city')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@city_router.post('/', response_model=CityOutSchema, tags=['City'], summary='Create city')
async def create_city(city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.get('/', response_model=List[CityOutSchema], summary='Get all cities', tags=['City'])
async def cities_list(db: Session = Depends(get_db)):
    cities_db = db.query(City).all()
    if not cities_db:
        raise HTTPException(detail='No cities.', status_code=404)
    return cities_db

@city_router.get('/{city_id}/', response_model=CityOutSchema, summary='Get city by id', tags=['City'])
async def city_detail(city_id: int, db: Session = Depends(get_db)):
    city_db1 = db.query(City).filter(City.id==city_id).first()
    if not city_db1:
        raise HTTPException(detail='No city by this id.', status_code=404)
    return city_db1

@city_router.put('/{city_id}/', response_model=dict, summary='Change city', tags=['City'])
async def city_update(city_id: int, city: CityInputSchema, db: Session = Depends(get_db)):
    city_db2 = db.query(City).filter(City.id==city_id).first()
    if not city_db2:
        raise HTTPException(detail='No city by this id.', status_code=404)
    for key, value in city.model_dump().items():
        setattr(city_db2, key, value)
    db.commit()
    db.refresh(city_db2)
    return {'detail': 'City has been changed.'}

@city_router.delete('/{city_id}/', response_model=dict, summary='Delete city', tags=['City'])
async def city_delete(city_id: int, db: Session = Depends(get_db)):
    city_db3 = db.query(City).filter(City.id==city_id).first()
    if not city_db3:
        raise HTTPException(detail='No city by this id.', status_code=404)
    db.delete(city_db3)
    db.commit()
    return {'detail': 'City has been deleted.'}