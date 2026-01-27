from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional, List
from datetime import date

class StatusChoices(str, Enum):
    seller = 'Seller'
    buyer = 'Buyer'

class PropertyChoices(str, Enum):
    apartment = 'Apartment'
    house = 'house'
    commercial_real_estate = 'Commercial real estate'
    room = 'Room'
    plot = 'Plot'
    cottage = 'Cottage'
    garage_parking = 'Garage/Parking'

class RegionChoices(str, Enum):
    bishkek = 'Bishkek'
    osh = 'Osh'
    chui = 'Chui'
    jalal_abad = 'Jalal-Abad'
    naryn = 'Naryn'
    issyk_kul = 'Issyk-Kul'
    talas = 'Talas'

class ConditionChoices(str, Enum):
    for_finishing = 'For finishing'
    euro = 'European style renovation'
    good = 'Good'
    middle = 'Middle'
    not_finished = 'Not finished'

class UserProfileLoginSchema(BaseModel):
    username: str
    password: str

class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: StatusChoices
    data_registered: date
class UserProfileInputSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6)
    email: EmailStr
    status: StatusChoices

class CityOutSchema(BaseModel):
    id: int
    city_name: str
class CityInputSchema(BaseModel):
    city_name: str = Field(max_length=64)

class DistrictOutSchema(BaseModel):
    id: int
    district_name: str
class DistrictInputSchema(BaseModel):
    district_name: str = Field(max_length=64)

class PropertyOutSchema(BaseModel):
    id: int
    title: str
    description: str
    property_type: PropertyChoices
    region: RegionChoices
    city_id: int
    district_id: int
    address: str
    area: int
    price: int
    rooms: int
    floor: int
    total_floors: int
    condition: ConditionChoices
    images: str
    documents: str
    seller_id: int
    created_date: date
class PropertyInputSchema(BaseModel):
    title: str
    description: str
    property_type: PropertyChoices
    region: RegionChoices
    city_id: int
    district_id: int
    address: str = Field(max_length=100)
    area: int = Field(le=100)
    price: int
    rooms: int = Field(le=100)
    floor: int = Field(le=100)
    total_floors: int = Field(le=300)
    condition: ConditionChoices
    images: str
    documents: str
    seller_id: int

class ReviewOutSchema(BaseModel):
    id: int
    buyer_id: int
    seller_id: int
    rating: int
    comment: str
    created_date: date
class ReviewInputSchema(BaseModel):
    buyer_id: int
    seller_id: int
    rating: int = Field(ge=0, le=10)
    comment: str = Field(max_length=100)

class HousePredictSchema(BaseModel):
    GrLivArea: int
    YearBuilt: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    OverallQual: int
    Neighborhood: str