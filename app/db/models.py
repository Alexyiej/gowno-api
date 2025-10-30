
from sqlalchemy import (
    Column, Integer, String, Boolean, DECIMAL, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .connection import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    lat = Column(DECIMAL(9, 6), nullable=False)
    long = Column(DECIMAL(9, 6), nullable=False)
    is_hub = Column(Boolean, default=False)

    current_vehicles = relationship("Vehicle", back_populates="current_location")
    start_segments = relationship("Segment", foreign_keys="Segment.start_loc_id", back_populates="start_location")
    end_segments = relationship("Segment", foreign_keys="Segment.end_loc_id", back_populates="end_location")
    loc_relations1 = relationship("LocationRelation", foreign_keys="LocationRelation.id_loc_1", back_populates="loc1")
    loc_relations2 = relationship("LocationRelation", foreign_keys="LocationRelation.id_loc_2", back_populates="loc2")


class LocationRelation(Base):
    __tablename__ = "location_relations"

    id = Column(Integer, primary_key=True)
    id_loc_1 = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    id_loc_2 = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    dist = Column(DECIMAL(10, 3), nullable=False)
    time = Column(DECIMAL(10, 2), nullable=False)

    loc1 = relationship("Location", foreign_keys=[id_loc_1], back_populates="loc_relations1")
    loc2 = relationship("Location", foreign_keys=[id_loc_2], back_populates="loc_relations2")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    registration_number = Column(String(32), unique=True, nullable=False)
    brand = Column(String(100))
    service_interval_km = Column(Integer)
    leasing_start_km = Column(Integer)
    leasing_limit_km = Column(Integer)
    leasing_start_date = Column(TIMESTAMP)
    leasing_end_date = Column(TIMESTAMP)
    current_odometer_km = Column(Integer)
    current_location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))

    current_location = relationship("Location", back_populates="current_vehicles")
    routes = relationship("Route", back_populates="vehicle")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    start_datetime = Column(TIMESTAMP, nullable=False)
    end_datetime = Column(TIMESTAMP, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"))
    is_test_set = Column(Boolean, default=False)

    vehicle = relationship("Vehicle", back_populates="routes")
    segments = relationship("Segment", back_populates="route", cascade="all, delete")


class Segment(Base):
    __tablename__ = "segments"

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    seq = Column(Integer, nullable=False)
    start_loc_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    end_loc_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    start_datetime = Column(TIMESTAMP)
    end_datetime = Column(TIMESTAMP)
    distance_travelled_km = Column(Integer)
    relation_id = Column(Integer, ForeignKey("location_relations.id"))

    route = relationship("Route", back_populates="segments")
    start_location = relationship("Location", foreign_keys=[start_loc_id], back_populates="start_segments")
    end_location = relationship("Location", foreign_keys=[end_loc_id], back_populates="end_segments")
    relation = relationship("LocationRelation")






class RecommendedRoute(Base):
    __tablename__ = "recommended_routes"

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"))
    start_loc_id = Column(Integer, ForeignKey("locations.id"))
    end_loc_id = Column(Integer, ForeignKey("locations.id"))
    planned_start = Column(TIMESTAMP)
    planned_end = Column(TIMESTAMP)
    distance_km = Column(Integer)
    duration_min = Column(Integer)
