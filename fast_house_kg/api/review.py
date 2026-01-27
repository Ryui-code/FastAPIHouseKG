from fast_house_kg.database.schema import ReviewOutSchema, ReviewInputSchema
from fast_house_kg.database.models import Review
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from fast_house_kg.database.db import SessionLocal

review_router = APIRouter(prefix='/review')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/', response_model=ReviewOutSchema, tags=['Review'], summary='Create review')
async def create_review(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/', response_model=List[ReviewOutSchema], summary='Get all reviews', tags=['Review'])
async def reviews_list(db: Session = Depends(get_db)):
    reviews_db = db.query(Review).all()
    if not reviews_db:
        raise HTTPException(detail='No reviews.', status_code=404)
    return reviews_db

@review_router.get('/{review_id}/', response_model=ReviewOutSchema, summary='Get review by id', tags=['Review'])
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review_db1 = db.query(Review).filter(Review.id == review_id).first()
    if not review_db1:
        raise HTTPException(detail='No review by this id.', status_code=404)
    return review_db1

@review_router.put('/{review_id}/', response_model=dict, summary='Change review', tags=['Review'])
async def review_update(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db2 = db.query(Review).filter(Review.id == review_id).first()
    if not review_db2:
        raise HTTPException(detail='No review by this id.', status_code=404)
    for key, value in review.model_dump().items():
        setattr(review_db2, key, value)
    db.commit()
    db.refresh(review_db2)
    return {'detail': 'Review has been changed.'}

@review_router.delete('/{review_id}/', response_model=dict, summary='Delete review', tags=['Review'])
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review_db3 = db.query(Review).filter(Review.id == review_id).first()
    if not review_db3:
        raise HTTPException(detail='No review by this id.', status_code=404)
    db.delete(review_db3)
    db.commit()
    return {'detail': 'Review has been deleted.'}