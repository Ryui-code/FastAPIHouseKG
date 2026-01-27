from sqladmin import Admin
from fast_house_kg.database.db import engine
from .views import *
from fastapi import FastAPI

def admin_setup(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(UserProfileRefreshTokenAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(DistrictAdmin)
    admin.add_view(PropertyAdmin)
    admin.add_view(ReviewAdmin)