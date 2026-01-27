from fast_house_kg.database.schema import DistrictOutSchema, DistrictInputSchema
from fast_house_kg.database.models import District
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from fast_house_kg.database.db import SessionLocal

district_router = APIRouter(prefix='/district')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@district_router.post('/', response_model=DistrictOutSchema, tags=['District'], summary='Create district')
async def create_district(district: DistrictInputSchema, db: Session = Depends(get_db)):
    district_db = District(**district.dict())
    db.add(district_db)
    db.commit()
    db.refresh(district_db)
    return district_db

@district_router.get('/', response_model=List[DistrictOutSchema], summary='Get all districts', tags=['District'])
async def districts_list(db: Session = Depends(get_db)):
    district_db = db.query(District).all()
    if not district_db:
        raise HTTPException(detail='No districts.', status_code=404)
    return district_db

@district_router.get('/{district_id}/', response_model=DistrictOutSchema, summary='Get district by id', tags=['District'])
async def district_detail(district_id: int, db: Session = Depends(get_db)):
    districts_db1 = db.query(District).filter(District.id == district_id).first()
    if not districts_db1:
        raise HTTPException(detail='No district by this id.', status_code=404)
    return districts_db1

@district_router.put('/{district_id}/', response_model=dict, summary='Change district', tags=['District'])
async def district_update(district_id: int, district: DistrictInputSchema, db: Session = Depends(get_db)):
    district_db2 = db.query(District).filter(District.id == district_id).first()
    if not district_db2:
        raise HTTPException(detail='No district by this id.', status_code=404)
    for key, value in district.model_dump().items():
        setattr(district_db2, key, value)
    db.commit()
    db.refresh(district_db2)
    return {'detail': 'District has been changed.'}

@district_router.delete('/{district_id}/', response_model=dict, summary='Delete district', tags=['District'])
async def district_delete(district_id: int, db: Session = Depends(get_db)):
    district_db3 = db.query(District).filter(District.id == district_id).first()
    if not district_db3:
        raise HTTPException(detail='No district by this id.', status_code=404)
    db.delete(district_db3)
    db.commit()
    return {'detail': 'District has been deleted.'}