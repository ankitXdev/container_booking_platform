from sqlalchemy import String, Integer, Column, ForeignKey
from app.config.database import Base
from sqlalchemy.orm import relationship

class provider_details(Base):
    __tablename__ = "provider_details"

    provider_id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    business_name = Column(String, nullable=False)
    business_address = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    approval_status = Column(String, default="pending")

    user = relationship("users")
