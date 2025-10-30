from sqlalchemy import Table, Column, Integer, String, DECIMAL, MetaData, Date 
from .connection import engine
metadata = MetaData()

table = Table('planned_routes', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('route_id', Integer, nullable=False),
    Column('vehicle_id', Integer, nullable=False),
    Column('registration_plate', String(32), nullable=False),
    Column('route_sequence', Integer, nullable=False),
    Column('location_start_id', Integer, nullable=False),
    Column('location_end_id', Integer, nullable=False),
    Column('distance_km', DECIMAL(10,2)),
    Column('planned_date', Date, nullable=False)
)

def create_table():
    metadata.create_all(engine)

