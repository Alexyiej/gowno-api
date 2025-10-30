import json
from app.data.load_data import load_csvs

def number_of_changes():
    _, _, segments_df, _, _ = load_csvs()
    changes_per_route = segments_df.groupby("route_id").size() - 1
    total_changes = changes_per_route[changes_per_route > 0].sum()
    result = {"total_changes": int(total_changes)}
    return json.dumps(result)

if __name__ == "__main__":
    print(number_of_changes())
