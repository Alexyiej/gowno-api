
import pandas as pd
import numpy as np

def clean_data(vehicles, locations, segments, location_relations=None):
    for df in [vehicles, locations, segments]:
        df.columns = df.columns.str.strip().str.lower()

    if location_relations is not None:
        location_relations.columns = location_relations.columns.str.strip().str.lower()

        if 'relation_id' in segments.columns and 'id' in location_relations.columns:
            segments = segments.merge(
                location_relations[['id', 'dist']],
                how='left',
                left_on='relation_id',
                right_on='id'
            )
            segments.rename(columns={'dist': 'distance_travelled_km'}, inplace=True)
            segments.drop(columns=['id_y'], errors='ignore', inplace=True)
            segments.rename(columns={'id_x': 'id'}, inplace=True)

    return vehicles, locations, segments

def location_stats(segments, locations):
    start_counts = segments.groupby('start_loc_id').size().reset_index(name='start_count')
    
    end_counts = segments.groupby('end_loc_id').size().reset_index(name='end_count')
    
    avg_distance = segments.groupby('start_loc_id')['distance_travelled_km'].mean().reset_index(name='avg_distance')
    
    loc_stats = locations.merge(start_counts, left_on='id', right_on='start_loc_id', how='left')
    loc_stats = loc_stats.merge(end_counts, left_on='id', right_on='end_loc_id', how='left')
    loc_stats = loc_stats.merge(avg_distance, left_on='id', right_on='start_loc_id', how='left')
    
    loc_stats.fillna(0, inplace=True)
    
    loc_stats = loc_stats[['id', 'name', 'lat', 'long', 'is_hub', 'start_count', 'end_count', 'avg_distance']]
    
    return loc_stats

def prepare_vrp_matrix(locations_rel, location_stats):
    n = len(location_stats)
    distance_matrix = np.zeros((n, n))
    
    for _, row in locations_rel.iterrows():
        try:
            i = location_stats[location_stats['id'] == row['id_loc_1']].index[0]
            j = location_stats[location_stats['id'] == row['id_loc_2']].index[0]
            distance_matrix[i, j] = row['dist']
            distance_matrix[j, i] = row['dist']  # undirected
        except IndexError:
            continue
    
    return distance_matrix
