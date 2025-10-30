from app.data.load_data import load_csvs

def driver_changes_top5():
    _, _, segments_df, routes_df, _ = load_csvs()

    changes_per_route = segments_df.groupby("route_id").size() - 1

    vehicle_changes = {}
    for route_id, changes in changes_per_route.items():
        if route_id not in routes_df["id"].values:
            continue
        vehicle_id = routes_df.loc[routes_df["id"] == route_id, "id"].iloc[0]  
        vehicle_changes[vehicle_id] = vehicle_changes.get(vehicle_id, 0) + max(changes, 0)

    top5 = sorted(vehicle_changes.items(), key=lambda x: x[1], reverse=True)[:5]

    chart_data = []
    for vehicle_id, changes in top5:
        chart_data.append({
            "label": f"Vehicle {vehicle_id}",
            "value": changes
        })

    return chart_data

