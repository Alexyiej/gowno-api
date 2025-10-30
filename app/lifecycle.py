
# app/lifecycle.py
import traceback
from db.planned_routes import create_table, table
from db.connection import engine
from data.load_data import load_csvs
from routing.preprocessing import clean_data, location_stats, prepare_vrp_matrix
from routing.clustering import perform_clustering
from routing.solve_vrp import solve_vrp
from kpi.kpi import calculate_and_store_kpis
# -------------------------------
# Step 0: DB initialization
# -------------------------------
async def init_db():
    """Create planned_routes table if not exists"""
    create_table()

# -------------------------------
# Step 1: Load, process data & save VRP routes
# -------------------------------
async def load_and_process_data():
    locations, vehicles, segments, routes_df, locations_rel = load_csvs()

    # Ensure correct types
    vehicles['id'] = vehicles['id'].astype(int)
    locations['id'] = locations['id'].astype(int)
    routes_df['id'] = routes_df['id'].astype(int)
    routes_df['distance_km'] = routes_df['distance_km'].astype(float)

    # Preprocess
    vehicles, locations, segments = clean_data(vehicles, locations, segments, locations_rel)
    loc_stats = location_stats(segments, locations)
    loc_stats = perform_clustering(loc_stats, n_clusters=5)

    # Prepare VRP
    distance_matrix = prepare_vrp_matrix(locations_rel, loc_stats)
    vrp_solutions = solve_vrp(distance_matrix, num_vehicles=len(vehicles))
    routes_ids = [[loc_stats.iloc[i]['id'] for i in route] for route in vrp_solutions]

    # Save routes to DB
    with engine.begin() as conn:
        for v_idx, route in enumerate(routes_ids):
            vehicle_id = int(vehicles.iloc[v_idx]['id'])
            reg_plate = str(vehicles.iloc[v_idx]['registration_number'])

            if v_idx < len(routes_df):
                route_id = int(routes_df.iloc[v_idx]['id'])
                distance = float(routes_df.iloc[v_idx]['distance_km'])
            else:
                route_id, distance = None, None

            for seq in range(len(route) - 1):
                start_loc = int(route[seq])
                end_loc = int(route[seq + 1])

                try:
                    conn.execute(table.insert(), {
                        "vehicle_id": vehicle_id,
                        "registration_plate": reg_plate,
                        "route_id": route_id,
                        "route_sequence": int(seq),
                        "location_start_id": start_loc,
                        "location_end_id": end_loc,
                        "distance_km": distance
                    })
                except Exception:
                    print(f"Error inserting row: vehicle {vehicle_id}, seq {seq}")
                    traceback.print_exc()


# -------------------------------
# Step 3: Run all startup tasks sequentially
# -------------------------------
async def run_startup_tasks():
    """Call this from FastAPI lifespan"""
    await init_db()
    await load_and_process_data()
    await calculate_and_store_kpis()
