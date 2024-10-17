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
    parser.add_argument(
        "--table_name",
        required=True,
        help="name of the table where we will write the results to",
    )
    parser.add_argument("--url", required=True, help="url of the csv file")
    args = parser.parse_args()

    # Download data
    filename = "output.parquet"
    os.system(f"wget {args.url} -O {filename}")

    # Ingest data into database
    df = pd.read_parquet(filename)
    engine = create_engine(
        f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.db}"
    )

    df.head(n=0).to_sql(name=args.table_name, con=engine, if_exists="replace")
    df.to_sql(name=args.table_name, con=engine, if_exists="append")
