from fast_house_kg.database.models import *
from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [i.key for i in UserProfile.__mapper__.columns]

class UserProfileRefreshTokenAdmin(ModelView, model=UserProfileRefreshToken):
    column_list = [i.key for i in UserProfileRefreshToken.__mapper__.columns]

class CityAdmin(ModelView, model=City):
    column_list = [i.key for i in City.__mapper__.columns]

class DistrictAdmin(ModelView, model=District):
    column_list = [i.key for i in District.__mapper__.columns]

class PropertyAdmin(ModelView, model=Property):
    column_list = [i.key for i in Property.__mapper__.columns]

class ReviewAdmin(ModelView, model=Review):
    column_list = [i.key for i in Review.__mapper__.columns]