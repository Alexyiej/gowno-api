import pandas as pd

def load_csvs():
    # Load all CSV files
    locations_df = pd.read_csv("locations.csv")
    vehicles_df = pd.read_csv("vehicles.csv")
    segments_df = pd.read_csv("segments.csv")
    routes_df = pd.read_csv("routes.csv")
    location_relations_df = pd.read_csv("locations_relations.csv")

    for df in [locations_df, vehicles_df, segments_df, routes_df, location_relations_df]:
        df.columns = df.columns.str.strip().str.lower()

    return locations_df, vehicles_df, segments_df, routes_df, location_relations_df