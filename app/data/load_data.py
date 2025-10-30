# routing/load_data.py
import pandas as pd

def load_csvs():
    """Load all CSV data and normalize column names, filtering segments and routes by start_datetime >= 01/01/2025."""
    date_filter = pd.to_datetime("2025-01-01")

    def load_csv(file_path, filter_date=False):
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()  # normalize columns
        if filter_date and 'start_datetime' in df.columns:
            df['start_datetime'] = pd.to_datetime(df['start_datetime'], errors='coerce')
            df = df[df['start_datetime'] >= date_filter]
        return df

    locations_df = load_csv("data/locations.csv")
    vehicles_df = load_csv("data/vehicles.csv")
    segments_df = load_csv("data/segments.csv", filter_date=True)
    routes_df = load_csv("data/routes.csv", filter_date=True)
    location_relations_df = load_csv("data/locations_relations.csv")

    return locations_df, vehicles_df, segments_df, routes_df, location_relations_df
