import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@database:5432/ny_taxi")
taxi_zone = pd.read_csv("taxi_zone_lookup.csv")
trip_data = pd.read_csv("green_tripdata_2019-10.csv.gz")

with engine.connect() as connection:
    taxi_zone.to_sql(
        name="zone",
        con=connection,
        if_exists="replace",
        index=False,
        index_label="LocationID",
    )
    trip_data.to_sql(
        name="trip",
        con=connection,
        if_exists="replace",
        index=True,
    )
