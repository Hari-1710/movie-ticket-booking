from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(String)
    price = Column(Integer)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user = Column(String)
    movie = Column(String)
    seats = Column(String)
    amount = Column(Integer)
    date = Column(String)
