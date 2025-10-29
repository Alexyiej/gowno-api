import pandas as pd

def load_csvs():
    # Load all CSV files
    locations_df = pd.read_csv("data/locations.csv")
    vehicles_df = pd.read_csv("data/vehicles.csv")
    segments_df = pd.read_csv("data/segments.csv")
    routes_df = pd.read_csv("data/routes.csv")
    location_relations_df = pd.read_csv("data/locations_relations.csv")

    for df in [locations_df, vehicles_df, segments_df, routes_df, location_relations_df]:
        df.columns = df.columns.str.strip().str.lower()

    return locations_df, vehicles_df, segments_df, routes_df, location_relations_df


if __name__ == "__main__":
    locations_df, vehicles_df, segments_df, routes_df, location_relations_df = load_csvs()
    (
        locations_df,
        vehicles_df,
        segments_df,
        routes_df,
        location_relations_df,
    ) = preprocess_dataframes(locations_df, vehicles_df, segments_df, routes_df, location_relations_df)

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
