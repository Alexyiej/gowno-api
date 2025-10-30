import json
from app.data.load_data import load_csvs

def estimated_time_to_reach_limits():
    _, vehicles_df, routes_df, _, _ = load_csvs()
    vehicles_df["km_done"] = vehicles_df["current_odometer_km"]
    vehicles_df["km_remaining"] = vehicles_df["leasing_limit_km"] - vehicles_df["km_done"]
    vehicles_df["avg_km_per_day"] = 100 
    vehicles_df["days_to_limit"] = vehicles_df["km_remaining"] / vehicles_df["avg_km_per_day"]
    avg_days_to_limit = vehicles_df["days_to_limit"].mean()
    result = {"avg_days_to_limit": round(avg_days_to_limit, 2)}
    return json.dumps(result)

if __name__ == "__main__":
    print(estimated_time_to_reach_limits())
