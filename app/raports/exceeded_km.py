# app/kpis/exceeded_cost.py
from data.load_data import load_csvs
from db.connection import engine
from db.planned_routes import table
import pandas as pd

COST_NORMAL_KM = 1.92
COST_EXCEEDED_KM = 0.92  # extra per exceeded km

def calculate_exceeded_costs():
    # Load CSV data
    _, vehicles_df, _, _, _ = load_csvs()
    
    # Load planned routes distances from DB
    with engine.connect() as conn:
        routes_df = pd.read_sql(table.select(), conn)
    
    # Calculate total km driven per vehicle from planned_routes
    km_per_vehicle = routes_df.groupby("vehicle_id")["distance_km"].sum().reset_index()
    km_per_vehicle.rename(columns={"distance_km": "planned_km"}, inplace=True)
    
    # Merge with vehicles info from CSV
    df = vehicles_df.merge(km_per_vehicle, left_on="id", right_on="vehicle_id", how="left")
    
    # Fill NaN for vehicles without routes
    df["planned_km"] = df["planned_km"].fillna(0)
    
    # Calculate exceeded km
    df["exceeded_km"] = df["planned_km"] - df["leasing_limit_km"]
    df["exceeded_km"] = df["exceeded_km"].apply(lambda x: x if x > 0 else 0)
    
    # Calculate costs
    df["cost_normal"] = df["planned_km"] * COST_NORMAL_KM
    df["cost_exceeded"] = df["exceeded_km"] * COST_EXCEEDED_KM
    df["total_cost"] = df["cost_normal"] + df["cost_exceeded"]
    
    # Sort by exceeded km
    df = df.sort_values(by="exceeded_km", ascending=False)
    
    # Return all vehicles with total cost
    result = df[["registration_number", "planned_km", "exceeded_km", "total_cost"]]
    return result

if __name__ == "__main__":
    costs_df = calculate_exceeded_costs()
    print(costs_df.to_string(index=False))
