from fast_house_kg.database.schema import PropertyOutSchema, PropertyInputSchema
from fast_house_kg.database.models import Property
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from fast_house_kg.database.db import SessionLocal

property_router = APIRouter(prefix='/property')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@property_router.post('/', response_model=PropertyOutSchema, tags=['Property'], summary='Create property')
async def create_property(property: PropertyInputSchema, db: Session = Depends(get_db)):
    property_db = Property(**property.dict())
    db.add(property_db)
    db.commit()
    db.refresh(property_db)
    return property_db

@property_router.get('/', response_model=List[PropertyOutSchema], summary='Get all properties', tags=['Property'])
async def properties_list(db: Session = Depends(get_db)):
    properties_db = db.query(Property).all()
    if not properties_db:
        raise HTTPException(detail='No properties.', status_code=404)
    return properties_db

@property_router.get('/{property_id}/', response_model=PropertyOutSchema, summary='Get property by id', tags=['Property'])
async def property_detail(property_id: int, db: Session = Depends(get_db)):
    property_db1 = db.query(Property).filter(Property.id == property_id).first()
    if not property_db1:
        raise HTTPException(detail='No property by this id.', status_code=404)
    return property_db1

@property_router.put('/{property_id}/', response_model=dict, summary='Change property', tags=['Property'])
async def property_update(property_id: int, property: PropertyInputSchema, db: Session = Depends(get_db)):
    property_db2 = db.query(Property).filter(Property.id == property_id).first()
    if not property_db2:
        raise HTTPException(detail='No property by this id.', status_code=404)
    for key, value in property.model_dump().items():
        setattr(property_db2, key, value)
    db.commit()
    db.refresh(property_db2)
    return {'detail': 'Property has been changed.'}

@property_router.delete('/{property_id}/', response_model=dict, summary='Delete property', tags=['Property'])
async def property_delete(property_id: int, db: Session = Depends(get_db)):
    property_db3 = db.query(Property).filter(Property.id == property_id).first()
    if not property_db3:
        raise HTTPException(detail='No property by this id.', status_code=404)
    db.delete(property_db3)
    db.commit()
    return {'detail': 'Property has been deleted.'}