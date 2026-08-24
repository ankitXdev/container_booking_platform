from sqlalchemy import String, Integer, Column, ForeignKey
from app.config.database import Base

class provider_details(Base):
     __tablename__ = 'provider_details'
     provider_id = Column(Integer, primary_key=True)
     user_id = Column(Integer, ForeignKey("users.user_id"))
     business_name = Column(String(150), unique=True,nullable=False)
     business_address = Column(String(150), nullable=False)
     contact = Column(String(20), unique=True, nullable=False)
     approval_status = Column(String(20),nullable=False)




