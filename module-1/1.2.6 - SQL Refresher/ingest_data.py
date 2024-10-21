import os
from argparse import ArgumentParser

import pandas as pd
from sqlalchemy import create_engine

if __name__ == "__main__":
    parser = ArgumentParser(description="ingest data to Postgres")
    parser.add_argument("--user", required=True, help="user name for postgres")
    parser.add_argument("--password", required=True, help="password for postgres")
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument("--db", required=True, help="database name for postgres")
    parser.add_argument("--taxi_data_url", required=True, help="url of the csv file")
    parser.add_argument("--zone_data_url", required=True, help="url of the csv file")
    args = parser.parse_args()

    engine = create_engine(
        f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.db}"
    )

    # Download taxi data
    taxi_filename = "taxi.parquet"
    os.system(f"wget {args.taxi_data_url} -O {taxi_filename}")
    print("Download: Taxi Data")

    # Ingest taxi data into database
    df = pd.read_parquet(taxi_filename)
    df.head(n=0).to_sql(name="yellow_taxi_trips", con=engine, if_exists="replace")
    df.to_sql(name="yellow_taxi_trips", con=engine, if_exists="append")
    print("Ingest: Taxi Data")

    # Download zone data
    zone_filename = "taxi+_zone_lookup.csv"
    os.system(f"wget {args.zone_data_url} -O {zone_filename}")
    print("Download: Zone Data")

    # Ingest zone data into database
    df = pd.read_csv(zone_filename)
    df.head(n=0).to_sql(name="zones", con=engine, if_exists="replace")
    df.to_sql(name="zones", con=engine, if_exists="append")
    print("Ingest: Zone Data")
