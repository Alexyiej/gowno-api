from sqlalchemy import (
    Column, Integer, String, Boolean, DECIMAL, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .connection import Base

class Alert(Base):
    

    __tablename__ = "alerts"


    id = Column(Integer, primary_key=True)
    brand = Column(String(100))
    registration = Column(String(32))
    total_mileage = Column(DECIMAL)
    mileage_since_service = Column(DECIMAL)
    service_interval = Column(DECIMAL)
    yearly_mileage = Column(DECIMAL)
    contract_limit = Column(DECIMAL)
    description = Column(String(256))
