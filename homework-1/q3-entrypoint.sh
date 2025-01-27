#!/usr/bin/env bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

pip install sqlalchemy psycopg2 pandas pgcli
python /data-ingestion.py
pgcli postgresql://user:password@database:5432/ny_taxi
# tail -f /dev/null