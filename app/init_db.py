
# init_db.py
from db import Base, engine

# This will create all tables defined in Base.metadata
Base.metadata.create_all(engine)

print("Database tables created successfully!")
