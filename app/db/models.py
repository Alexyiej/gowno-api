from sqlalchemy import Column, Integer, String
from .connection import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    registration_number = Column(String(32), nullable=False)
    description = Column(String(256), nullable=False)
