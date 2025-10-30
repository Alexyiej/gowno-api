from sqlalchemy import text
from db.connection import engine



def calculate_and_store_kpis():
    """Calculate KPIs and insert into fleet_kpis table"""
    with engine.begin() as conn:
        # 1) Total route changes across all routes
        route_changes = conn.execute(text("""
            SELECT SUM(route_changes) FROM (
                SELECT route_id, COUNT(*) - 1 AS route_changes
                FROM planned_routes
                GROUP BY route_id
            ) t;
        """)).scalar() or 0

        # 2) Avg leasing contract utilization %
        contract_usage = conn.execute(text("""
            SELECT AVG((current_odometer_km::decimal / leasing_limit_km) * 100)
            FROM vehicles;
        """)).scalar() or 0.0

        # 3) % of vehicles below leasing limit
        percent_ok = conn.execute(text("""
            SELECT COUNT(*) FILTER (WHERE current_odometer_km <= leasing_limit_km)::float
                   / COUNT(*) * 100
            FROM vehicles;
        """)).scalar() or 0.0

        kpi_data = {
            "total_route_changes": int(route_changes),
            "avg_contract_utilization": round(contract_usage, 2),
            "percent_without_exceeding": round(percent_ok, 2)
        }

        # Insert KPI into DB
        conn.execute(text("""
            INSERT INTO fleet_kpis (
                total_route_changes,
                avg_contract_utilization,
                percent_without_exceeding
            )
            VALUES (:total_route_changes, :avg_contract_utilization, :percent_without_exceeding)
        """), kpi_data)

        print("✅ KPIs calculated and stored:", kpi_data)


calculate_and_store_kpis()
