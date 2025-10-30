# app/alerts/vehicle_alerts.py
from datetime import datetime
import pandas as pd
from sqlalchemy import Column, Integer, String, Float, DateTime, Table, MetaData
from sqlalchemy.orm import sessionmaker
from db.connection import engine
from data.load_data import load_csvs
from db.planned_routes import table as planned_table

# --- CONFIG ---
WARNING_THRESHOLD = 0.9
metadata = MetaData()
Session = sessionmaker(bind=engine)

# --- ALERTS TABLE ---
vehicle_alerts_table = Table(
    "vehicle_alerts", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("vehicle_id", Integer, nullable=False),
    Column("registration", String, nullable=False),
    Column("service_interval_km", Integer, nullable=False),
    Column("leasing_limit_km", Integer, nullable=False),
    Column("total_mileage", Float, nullable=False),
    Column("mileage_since_service", Float, nullable=False),
    Column("type", String, nullable=False),
    Column("description", String, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow)
)
metadata.create_all(engine)

# --- ALERT CALCULATION ---
def process_all_alerts():
    print("🚀 Starting alert processing...")
    session = Session()
    alerts_to_insert = []

    try:
        # Load vehicles CSV
        print("📥 Loading vehicles from CSV...")
        try:
            vehicles_df, *_ = load_csvs()  # only first DF
            vehicles_df.columns = vehicles_df.columns.str.strip().str.lower()  # normalize columns
            print(f"✅ Loaded {len(vehicles_df)} vehicles")
        except Exception as e:
            print(f"❌ Failed to load vehicles: {e}")
            return

        # Ensure vehicle_id column exists
        if 'id' in vehicles_df.columns:
            vehicles_df.rename(columns={'id': 'vehicle_id'}, inplace=True)
        elif 'vehicle_id' not in vehicles_df.columns:
            print("⚠️ No 'Id' or 'vehicle_id' column in vehicles CSV, cannot match planned routes")
            return

        # Load planned routes
        print("📥 Loading planned routes from DB...")
        try:
            planned_routes_df = pd.read_sql(planned_table.select(), engine)
            planned_routes_df['planned_date'] = pd.to_datetime(planned_routes_df['planned_date'], errors='coerce')
            print(f"✅ Loaded {len(planned_routes_df)} planned routes")
        except Exception as e:
            print(f"❌ Failed to load planned routes: {e}")
            return

        # Total mileage per vehicle from planned routes
        mileage_per_vehicle = planned_routes_df.groupby('vehicle_id')['distance_km'].sum().reset_index()
        mileage_per_vehicle = mileage_per_vehicle.rename(columns={'distance_km': 'total_mileage'})
        print("📊 Calculated total mileage per vehicle")

        # Merge vehicles with total mileage using vehicle_id
        vehicles_df = vehicles_df.merge(
            mileage_per_vehicle,
            on='vehicle_id',
            how='left'
        )
        vehicles_df['total_mileage'] = vehicles_df['total_mileage'].fillna(0)
        print("🔗 Merged vehicles with mileage")

        # Process alerts
        for idx, row in vehicles_df.iterrows():
            try:
                vehicle_id = row.get('vehicle_id')
                reg = row.get("registration_number", "UNKNOWN")
                odometer = float(row.get("current_odometer_km", 0))
                service_interval = float(row.get("service_interval_km", 10000))
                contract_limit = float(row.get("leasing_limit_km", 50000))
                total_mileage = odometer + float(row.get("total_mileage", 0))
                mileage_since_service = total_mileage % service_interval if service_interval > 0 else 0

                alert_base = {
                    'vehicle_id': vehicle_id,
                    'registration': reg,
                    'service_interval_km': service_interval,
                    'leasing_limit_km': contract_limit,
                    'total_mileage': total_mileage,
                    'mileage_since_service': mileage_since_service,
                    'created_at': datetime.utcnow()
                }

                # SERVICE ALERT
                if service_interval > 0:
                    if mileage_since_service >= service_interval:
                        alert = alert_base.copy()
                        alert.update({'type': 'SERWIS', 'description': 'Pojazd powinien być natychmiast serwisowany'})
                        alerts_to_insert.append(alert)
                    elif mileage_since_service >= service_interval * WARNING_THRESHOLD:
                        alert = alert_base.copy()
                        alert.update({'type': 'SERWIS', 'description': 'Pojazd będzie musiał być serwisowany wkrótce'})
                        alerts_to_insert.append(alert)

                # CONTRACT ALERT
                if total_mileage >= contract_limit:
                    alert = alert_base.copy()
                    alert.update({'type': 'KONTRAKT', 'description': 'Pojazd przekroczył limit kontraktowy'})
                    alerts_to_insert.append(alert)
                elif total_mileage >= contract_limit * WARNING_THRESHOLD:
                    alert = alert_base.copy()
                    alert.update({'type': 'KONTRAKT', 'description': 'Pojazd zbliża się do limitu kontraktowego'})
                    alerts_to_insert.append(alert)

            except Exception as e:
                print(f"❌ Failed to process vehicle row {idx} (vehicle_id={row.get('vehicle_id')}): {e}")

        # Insert alerts
        if alerts_to_insert:
            session.execute(vehicle_alerts_table.insert(), alerts_to_insert)
            session.commit()
            print(f"✅ Inserted {len(alerts_to_insert)} alerts into database")
        else:
            print("ℹ️ No alerts generated")

    except Exception as e:
        print(f"❌ Error during alert processing: {e}")

    finally:
        session.close()
        print("🏁 Alert processing finished")
