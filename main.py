from fastapi import FastAPI
import uvicorn
from fast_house_kg.admin.setup import admin_setup
from fast_house_kg.api import auth, users, city, district, property, review, predict

app = FastAPI()
app.include_router(predict.predict_router)
app.include_router(auth.auth_router)
app.include_router(users.users_router)
app.include_router(city.city_router)
app.include_router(district.district_router)
app.include_router(property.property_router)
app.include_router(review.review_router)

admin_setup(app)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)