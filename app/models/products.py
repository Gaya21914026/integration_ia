from sqlalchemy import  Column, Integer, String
from app.db.database import Base


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)
