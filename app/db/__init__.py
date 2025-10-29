
from db.connection import engine, Base, SessionLocal
from db.models import Location, Vehicle

# create all tables
Base.metadata.create_all(engine)

# Example: create a new location
with SessionLocal() as session:
    loc = Location(name="Warehouse", lat=52.5200, long=13.4050, is_hub=True)
    session.add(loc)
    session.commit()
    print(f"Added location with ID: {loc.id}")
