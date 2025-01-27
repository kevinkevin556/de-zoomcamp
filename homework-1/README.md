

# Module 1 Homework: Docker & SQL
https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/01-docker-terraform/homework.md

## Question 1. Understanding docker first run
Run `docker run -f q1_Dockerfile`.

```docker
FROM python:3.12.8
ENTRYPOINT ["bash"]
```
Ans: Version of pip = 24.3.1 = (1)

## Question 2. Understanding Docker networking and docker-compos
Run `docker compose -f q2-docker-compose.yaml up`

```yaml
services:
  db: # hostname = db
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432' # ports = 5432
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

Ans: db: 5432 = (2)

## Question 3. Trip Segmentation Count
Run `docker compose -f q3-docker-compose.yaml run --rm cli`

```sql
create view trip_within_period as (
  select index, trip_distance 
  from trip 
  where 
    lpep_dropoff_datetime::date >= '2019-10-01'::date and 
    lpep_dropoff_datetime::date < '2019-11-01'::date
)

select count(*) from trip_within_period where trip_distance <= 1 -- 104802

select count(*) from trip_within_period where trip_distance > 1 and trip_distance <= 3 -- 198924

select count(*) from trip_within_period where trip_distance > 3 and trip_distance <= 7 -- 109623  

select count(*) from trip_within_period where trip_distance > 7 and trip_distance <= 10 -- 27678

select count(*) from trip_within_period where trip_distance > 10 -- 35189
```
Ans: (2)


## Question 4. Longest trip for each day
```sql
select 
  lpep_pickup_datetime::date, 
  max(trip_distance)
from trip
group by lpep_pickup_datetime::date 
having 
  lpep_pickup_datetime::date in 
  ('2019-10-11'::date, '2019-10-24'::date, '2019-10-26'::date, '2019-10-31'::date)
```
```
+----------------------+--------+
| lpep_pickup_datetime | max    |
|----------------------+--------|
| 2019-10-26           | 91.56  |
| 2019-10-31           | 515.89 |
| 2019-10-24           | 90.75  |
| 2019-10-11           | 95.78  |
+----------------------+--------+
```
Ans: 2019-10-24 = (2)


## Question 5. Three biggest pickup zones
```sql
select "Zone", sum(total_amount) 
from trip 
inner join zone on "PULocationID" = "LocationID" 
where lpep_pickup_datetime::date = '2019-10-18'::date 
group by "Zone" 
having sum(total_amount) > 13000 
```

```
+---------------------+--------------------+
| Zone                | sum                |
|---------------------+--------------------|
| East Harlem North   | 18686.680000000088 |
| East Harlem South   | 16797.260000000068 |
| Morningside Heights | 13029.790000000034 |
+---------------------+--------------------+
```
Ans: (1)

## Question 6. Largest tip
```sql
select 
  d_zone."Zone",
  max(tip_amount)
from trip 
left join zone as p_zone on "PULocationID" = p_zone."LocationID"
left join zone as d_zone on "DOLocationID" = d_zone."LocationID"
where 
  lpep_pickup_datetime::date >= '2019-10-01'::date and
  lpep_pickup_datetime::date <= '2019-10-31'::date and
  p_zone."Zone" = 'East Harlem North'
group by d_zone."Zone"
order by max(tip_amount) desc
limit 1
```

```
+-------------+------+
| Zone        | max  |
|-------------+------|
| JFK Airport | 87.3 |
+-------------+------+
```
Ans: (2)


## Question 7. Terraform Workflow

Ans: terraform init, terraform apply -auto-approve, terraform destroy = (4) 