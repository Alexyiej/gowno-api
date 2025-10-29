
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def perform_clustering(location_stats, n_clusters=5, plot=False):
    coords = location_stats[['lat', 'long']].values
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    location_stats['region'] = kmeans.fit_predict(coords)
    
    if plot:
        plt.figure(figsize=(8,6))
        plt.scatter(location_stats['long'], location_stats['lat'], c=location_stats['region'], cmap='tab10', s=50)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Location Clusters')
        plt.colorbar(label='Region')
        plt.show()
    
    return location_stats

def save_clusters(location_stats, filename="outputs/region_clusters.csv"):
    location_stats.to_csv(filename, index=False)
