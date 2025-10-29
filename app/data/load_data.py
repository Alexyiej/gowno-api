import pandas as pd

def load_csvs():
    # Load all CSV files
    locations_df = pd.read_csv("data/locations.csv")
    vehicles_df = pd.read_csv("data/vehicles.csv")
    segments_df = pd.read_csv("data/segments.csv")
    routes_df = pd.read_csv("data/routes.csv")
    location_relations_df = pd.read_csv("data/locations_relations.csv")

    # Normalize headers (remove spaces, lowercase)
    for df in [locations_df, vehicles_df, segments_df, routes_df, location_relations_df]:
        df.columns = df.columns.str.strip().str.lower()

    return locations_df, vehicles_df, segments_df, routes_df, location_relations_df


def preprocess_dataframes(locations_df, vehicles_df, segments_df, routes_df, location_relations_df):
    # --- Clean locations ---
    locations_df["is_hub"] = locations_df["is_hub"].fillna(0).astype(bool)
    locations_df["lat"] = pd.to_numeric(locations_df["lat"], errors="coerce")
    locations_df["long"] = pd.to_numeric(locations_df["long"], errors="coerce")

    # --- Clean vehicles ---
    vehicles_df["current_odometer_km"] = pd.to_numeric(
        vehicles_df.get("current_odometer_km", 0), errors="coerce"
    ).fillna(0).astype(int)

    # --- Clean segments ---
    for col in ["relation_id", "route_id", "seq", "start_loc_id", "end_loc_id"]:
        if col in segments_df.columns:
            segments_df[col] = pd.to_numeric(segments_df[col], errors="coerce")

    # Parse datetime columns if they exist
    for col in ["start_datetime", "end_datetime"]:
        if col in segments_df.columns:
            segments_df[col] = pd.to_datetime(segments_df[col], errors="coerce")

    # --- Clean routes ---
    for col in ["start_datetime", "end_datetime"]:
        if col in routes_df.columns:
            routes_df[col] = pd.to_datetime(routes_df[col], errors="coerce")

    routes_df["distance_km"] = pd.to_numeric(routes_df.get("distance_km", 0), errors="coerce")

    # --- Clean location relations ---
    location_relations_df["dist"] = pd.to_numeric(location_relations_df["dist"], errors="coerce")
    location_relations_df["time"] = pd.to_numeric(location_relations_df["time"], errors="coerce")
    for col in ["id_loc_1", "id_loc_2"]:
        if col in location_relations_df.columns:
            location_relations_df[col] = pd.to_numeric(location_relations_df[col], errors="coerce")

    return locations_df, vehicles_df, segments_df, routes_df, location_relations_df


if __name__ == "__main__":
    # Load and preprocess
    locations_df, vehicles_df, segments_df, routes_df, location_relations_df = load_csvs()
    (
        locations_df,
        vehicles_df,
        segments_df,
        routes_df,
        location_relations_df,
    ) = preprocess_dataframes(locations_df, vehicles_df, segments_df, routes_df, location_relations_df)

    # Display summaries
    print("\n--- LOCATIONS ---")
    print(locations_df.head(), "\n")

    print("--- VEHICLES ---")
    print(vehicles_df.head(), "\n")

    print("--- SEGMENTS ---")
    print(segments_df.head(), "\n")

    print("--- ROUTES ---")
    print(routes_df.head(), "\n")

    print("--- LOCATION RELATIONS ---")
    print(location_relations_df.head(), "\n")
