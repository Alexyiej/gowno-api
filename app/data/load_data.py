# routing/load_data.py
import pandas as pd

def load_csvs():
    """Load all CSV data and normalize column names."""
    locations_df = pd.read_csv("data/locations.csv")
    vehicles_df = pd.read_csv("data/vehicles.csv")
    segments_df = pd.read_csv("data/segments.csv")
    routes_df = pd.read_csv("data/routes.csv")
    location_relations_df = pd.read_csv("data/locations_relations.csv")

    # Normalize column names (lowercase, no spaces)
    for df in [locations_df, vehicles_df, segments_df, routes_df, location_relations_df]:
        df.columns = df.columns.str.strip().str.lower()

    return locations_df, vehicles_df, segments_df, routes_df, location_relations_df
