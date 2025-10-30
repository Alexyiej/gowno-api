
from db.connection import engine
from db.planned_routes import table 

def save_routes_to_db(routes_ids, vehicles_df, locations_rel):
    with engine.begin() as conn:  # auto-commit
        for v_idx, route in enumerate(routes_ids):
            vehicle_id = int(vehicles_df.iloc[v_idx]['id'])
            reg_plate = str(vehicles_df.iloc[v_idx]['registration_number'])
            for seq in range(len(route)-1):
                start_loc = int(route[seq])
                end_loc = int(route[seq+1])
                dist_row = locations_rel[
                    ((locations_rel['id_loc_1']==start_loc)&(locations_rel['id_loc_2']==end_loc))|
                    ((locations_rel['id_loc_2']==start_loc)&(locations_rel['id_loc_1']==end_loc))
                ]
                distance = float(dist_row['dist'].iloc[0]) if not dist_row.empty else None

                row = {
                    "vehicle_id": vehicle_id,
                    "registration_plate": reg_plate,
                    "route_sequence": int(seq),
                    "location_start_id": start_loc,
                    "location_end_id": end_loc,
                    "distance_km": distance
                }
                print(f"Inserting: {row}")  # <-- debug
                conn.execute(table.insert(), row)
    print("Routes saved to DB successfully!")
