import json
from app.data.load_data import load_csvs

def percentage_of_vehicles_without_exceeding_the_limits():
    _, vehicles_df, _, _, _ = load_csvs()
    vehicles_df["within_limit"] = vehicles_df["current_odometer_km"] <= vehicles_df["leasing_limit_km"]
    percent_without_exceeding = vehicles_df["within_limit"].mean() * 100
    result = {"percent_without_exceeding": round(percent_without_exceeding, 2)}
    return json.dumps(result)

if __name__ == "__main__":
    print(percentage_of_vehicles_without_exceeding_the_limits())
