from database import Base
from sqlalchemy import Column,String,Integer

class Forms(Base):
    __tablename__="Forms"
    id=Column(Integer,primary_key=True,autoincrement=True)
    first_name= Column(String,nullable=True)
    last_name= Column(String,nullable=True)
    phone_number= Column(String,nullable=True)
    email= Column(String,nullable=True)
    gender= Column(String,nullable=True)
    city= Column(String,nullable=True)