from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Date, Text, Enum
from typing import List
from enum import Enum as PyEnum
from datetime import date

class StatusChoices(str, PyEnum):
    seller = 'Seller'
    buyer = 'Buyer'

class PropertyChoices(str, PyEnum):
    apartment = 'Apartment'
    house = 'house'
    commercial_real_estate = 'Commercial real estate'
    room = 'Room'
    plot = 'Plot'
    cottage = 'Cottage'
    garage_parking = 'Garage/Parking'

class RegionChoices(str, PyEnum):
    bishkek = 'Bishkek'
    osh = 'Osh'
    chui = 'Chui'
    jalal_abad = 'Jalal-Abad'
    naryn = 'Naryn'
    issyk_kul = 'Issyk-Kul'
    talas = 'Talas'

class ConditionChoices(str, PyEnum):
    for_finishing = 'For finishing'
    euro = 'European style renovation'
    good = 'Good'
    middle = 'Middle'
    not_finished = 'Not finished'

class UserProfile(Base):
    __tablename__ = 'user_profile'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.buyer)
    data_registered: Mapped[date] = mapped_column(Date, default=date.today)

    seller_property: Mapped[List['Property']] = relationship(back_populates='seller',
                                                             cascade='all, delete-orphan')
    review_buyer: Mapped[List['Review']] = relationship(back_populates='buyer',
                                                      cascade='all, delete-orphan', foreign_keys='Review.buyer_id')
    review_seller: Mapped[List['Review']] = relationship(back_populates='seller',
                                                         cascade='all, delete-orphan', foreign_keys='Review.seller_id')
    users_token: Mapped[List['UserProfileRefreshToken']] = relationship(
        back_populates='token_user',
        cascade='all, delete-orphan'
    )

class UserProfileRefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[date] = mapped_column(Date, default=date.today())

    token_user: Mapped[UserProfile] = relationship(back_populates='users_token')

class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String)

    city_property: Mapped[List['Property']] = relationship(back_populates='city',
                                                           cascade='all, delete-orphan')

class District(Base):
    __tablename__ = 'district'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    district_name: Mapped[str] = mapped_column(String)

    district_property: Mapped[List['Property']] = relationship(back_populates='district',
                                                               cascade='all, delete-orphan')

class Property(Base):
    __tablename__ = 'property'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    property_type: Mapped[PropertyChoices] = mapped_column(Enum(PropertyChoices), default=PropertyChoices.apartment)
    region: Mapped[RegionChoices] = mapped_column(Enum(RegionChoices), default=RegionChoices.bishkek)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'))
    address: Mapped[str] = mapped_column(String)
    area: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    rooms: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    total_floors: Mapped[int] = mapped_column(Integer)
    condition: Mapped[ConditionChoices] = mapped_column(Enum(ConditionChoices), default=ConditionChoices.good)
    images: Mapped[str] = mapped_column(String)
    documents: Mapped[str] = mapped_column(String)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    created_date: Mapped[date] = mapped_column(Date, default=date.today())

    city: Mapped[City] = relationship(back_populates='city_property')
    district: Mapped[District] = relationship(back_populates='district_property')
    seller: Mapped[UserProfile] = relationship(back_populates='seller_property')

class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_date: Mapped[date] = mapped_column(Date, default=date.today())

    buyer: Mapped[UserProfile] = relationship(back_populates='review_buyer', foreign_keys=[buyer_id])
    seller: Mapped[UserProfile] = relationship(back_populates='review_seller', foreign_keys=[seller_id])