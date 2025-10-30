import pandas as pd
from datetime import datetime
from load_data import load_csvs  # Twój plik load_data.py

# --- KONFIGURACJA --- #
WARNING_THRESHOLD = 0.9  # 90% limitu przed alertem ostrzegawczym

# --- FUNKCJE --- #

def calculate_yearly_mileage(segments_df, routes_df, current_date):
    """Oblicza przebieg pojazdów od początku bieżącego roku na podstawie tras zakończonych przed current_date."""
    current_year = current_date.year
    routes_df["start_datetime"] = pd.to_datetime(routes_df["start_datetime"], errors="coerce")
    routes_df["end_datetime"] = pd.to_datetime(routes_df["end_datetime"], errors="coerce")

    # Filtrujemy trasy zakończone przed current_date i w bieżącym roku
    completed_routes = routes_df[(routes_df["end_datetime"] <= current_date) & 
                                 (routes_df["end_datetime"].dt.year == current_year)]
    
    # Sumujemy przebiegi po pojazdach (po ID segmentów)
    if 'vehicle_id' not in segments_df.columns:
        # Jeśli nie ma vehicle_id w segmentach, zakładamy jeden pojazd na trasę w testach
        segments_df['vehicle_id'] = 1
    
    merged = segments_df.merge(completed_routes[['id', 'distance_km']], left_on='route_id', right_on='id', how='left')
    yearly_mileage = merged.groupby('vehicle_id')['distance_km'].sum().reset_index()
    yearly_mileage = yearly_mileage.rename(columns={'distance_km': 'total_mileage_year'})
    return yearly_mileage

def generate_alerts(reference_date: str):
    """Generuje alerty pojazdów, zamiast wysyłać je do bazy danych, zwraca listę i drukuje je."""
    current_date = pd.to_datetime(reference_date)

    # Wczytanie danych
    locations_df, vehicles_df, segments_df, routes_df, location_relations_df = load_csvs()

    # Oblicz roczny przebieg
    yearly_mileage_df = calculate_yearly_mileage(segments_df, routes_df, current_date)
    vehicles_df = vehicles_df.merge(yearly_mileage_df, left_on='id', right_on='vehicle_id', how='left')
    vehicles_df['total_mileage_year'] = vehicles_df['total_mileage_year'].fillna(0)

    alerts = []

    for _, row in vehicles_df.iterrows():
        brand = row.get("brand")
        reg = row.get("registration_number")
        odometer = row.get("current_odometer_km", 0)
        service_interval = row.get("service_interval_km", 10000)
        contract_limit = row.get("leasing_limit_km", 50000)
        yearly_mileage = row.get("total_mileage_year", 0)

        # Całkowity przebieg uwzględniający trasy od początku roku
        total_mileage = odometer + yearly_mileage
        mileage_since_service = total_mileage % service_interval

        # --- ALERT SERWISOWY ---
        if mileage_since_service >= service_interval:
            description = "Pojazd powinien być natychmiast serwisowany"
            alerts.append({
                'brand': brand,
                'registration': reg,
                'total_mileage': total_mileage,
                'mileage_since_service': mileage_since_service,
                'alert_type': 'SERWIS',
                'description': description
            })
        elif mileage_since_service >= service_interval * WARNING_THRESHOLD:
            description = "Pojazd będzie musiał być serwisowany wkrótce"
            alerts.append({
                'brand': brand,
                'registration': reg,
                'total_mileage': total_mileage,
                'mileage_since_service': mileage_since_service,
                'alert_type': 'SERWIS',
                'description': description
            })

        # --- ALERT KONTRAKTOWY ---
        if yearly_mileage >= contract_limit:
            description = "Pojazd przekroczył limit kontraktowy"
            alerts.append({
                'brand': brand,
                'registration': reg,
                'total_mileage': total_mileage,
                'mileage_since_service': mileage_since_service,
                'alert_type': 'KONTRAKT',
                'description': description
            })
        elif yearly_mileage >= contract_limit * WARNING_THRESHOLD:
            description = "Pojazd zbliża się do limitu kontraktowego"
            alerts.append({
                'brand': brand,
                'registration': reg,
                'total_mileage': total_mileage,
                'mileage_since_service': mileage_since_service,
                'alert_type': 'KONTRAKT',
                'description': description
            })

    return alerts

# --- TEST --- #
if __name__ == "__main__":
    reference_date = "2024-07-03"
    alerts = generate_alerts(reference_date)

    if not alerts:
        print("Brak alertów dla pojazdów w podanej dacie.")
    else:
        print(f"=== ALERTY POJAZDÓW dla {reference_date} ===")
        for a in alerts:
            print(a)
            print("---------------------------")
