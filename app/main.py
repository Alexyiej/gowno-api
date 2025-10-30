# from contextlib import asynccontextmanager
# import pandas as pd
# from fastapi import FastAPI
# from data.load_data import load_csvs
# from routing.preprocessing import clean_data, location_stats, prepare_vrp_matrix
# from routing.clustering import perform_clustering
# from routing.solve_vrp import solve_vrp
# from db.planned_routes import create_table, table
# from db.connection import engine
# import traceback
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # --- Step 0: Initialize DB table ---
#     create_table()
#
#     # --- Step 1: Load data ---
#     locations, vehicles, segments, routes_df, locations_rel = load_csvs()
#
#     # --- Ensure proper types ---
#     vehicles['id'] = vehicles['id'].astype(int)
#     locations['id'] = locations['id'].astype(int)
#     routes_df['id'] = routes_df['id'].astype(int)
#     routes_df['distance_km'] = routes_df['distance_km'].astype(float)
#
#     # --- Step 2: Preprocess ---
#     vehicles, locations, segments = clean_data(vehicles, locations, segments, locations_rel)
#     loc_stats = location_stats(segments, locations)
#
#     # --- Step 3: Clustering ---
#     loc_stats = perform_clustering(loc_stats, n_clusters=5)
#
#     # --- Step 4: Prepare VRP ---
#     distance_matrix = prepare_vrp_matrix(locations_rel, loc_stats)
#     vrp_solutions = solve_vrp(distance_matrix, num_vehicles=len(vehicles))
#     routes_ids = [[loc_stats.iloc[i]['id'] for i in route] for route in vrp_solutions]
#
#     # --- Step 5: Save results to DB with debugging ---
#     with engine.begin() as conn:  # <- use transaction to auto-commit
#         for v_idx, route in enumerate(routes_ids):
#             vehicle_id = int(vehicles.iloc[v_idx]['id'])
#             reg_plate = str(vehicles.iloc[v_idx]['registration_number'])
#
#             if v_idx < len(routes_df):
#                 route_id = int(routes_df.iloc[v_idx]['id'])
#                 distance = float(routes_df.iloc[v_idx]['distance_km'])
#             else:
#                 route_id = None
#                 distance = None
#
#             for seq in range(len(route)-1):
#                 start_loc = int(route[seq])
#                 end_loc = int(route[seq+1])
#
#                 data = {
#                     "vehicle_id": vehicle_id,
#                     "registration_plate": reg_plate,
#                     "route_id": route_id,
#                     "route_sequence": int(seq),
#                     "location_start_id": start_loc,
#                     "location_end_id": end_loc,
#                     "distance_km": distance
#                 }
#
#                 try:
#                     print(f"Trying to insert: {data}")  # Debug print
#                     conn.execute(table.insert(), data)
#                 except Exception as e:
#                     print("ERROR inserting row:")
#                     print(data)
#                     traceback.print_exc()
#
#     yield
#
#
# # --- FastAPI app ---
# app = FastAPI(title="VRP API", lifespan=lifespan)
#
# @app.get("/")
# def read_root():
#     return {"message": "VRP server running"}
#
# @app.get("/routes")
# def get_routes():
#     with engine.connect() as conn:
#         result = conn.execute(table.select())
#         return [dict(row._mapping) for row in result]






from fastapi import FastAPI
from contextlib import asynccontextmanager
from lifecycle import run_startup_tasks
from db.planned_routes import table
from db.connection import engine
from alerts.alerts_system import vehicle_alerts_table
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run everything on startup
    await run_startup_tasks()
    yield

app = FastAPI(title="VRP API", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "VRP server running"}

@app.get("/routes")
def get_routes():
    with engine.connect() as conn:
        result = conn.execute(table.select())
        return [dict(row._mapping) for row in result]
@app.get("/alerts")
def get_alerts():
    with engine.connect() as conn:
        result = conn.execute(select(vehicle_alerts_table))
        return [dict(row._mapping) for row in result]
