import json
from app.data.load_data import load_csvs

def percentage_of_contract_usage():
    _, vehicles_df, _, _, _ = load_csvs()
    vehicles_df["contract_utilization"] = (vehicles_df["current_odometer_km"] / vehicles_df["leasing_limit_km"]) * 100
    avg_utilization = vehicles_df["contract_utilization"].mean()
    result = {"avg_contract_utilization": round(avg_utilization, 2)}
    return json.dumps(result)

if __name__ == "__main__":
    print(percentage_of_contract_usage())
