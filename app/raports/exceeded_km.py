import json
from app.data.load_data import load_csvs

def exceeded_km_top5():
    _, vehicles_df, _, _, _ = load_csvs()

    vehicles_df["exceeded_km"] = vehicles_df["current_odometer_km"] - vehicles_df["leasing_limit_km"]
    vehicles_df["exceeded_km"] = vehicles_df["exceeded_km"].apply(lambda x: x if x > 0 else 0)

    top5_df = vehicles_df.sort_values(by="exceeded_km", ascending=False).head(5)

    chart_data = []
    for _, row in top5_df.iterrows():
        chart_data.append({
            "label": row["registration_number"],
            "value": row["exceeded_km"]
        })

    return json.dumps(chart_data, indent=4)

if __name__ == "__main__":
    print(exceeded_km_top5())
