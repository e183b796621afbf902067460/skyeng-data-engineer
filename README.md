# Skyeng Data Engineering Test Task

---

# Configuration

- Clone current repository:
```
git clone https://github.com/e183b796621afbf902067460/skyeng-data-engineer.git
```

- Get into the project folder:
```
cd skyeng-data-engineer/
```

# Deploy

All environment variables already set in [.env](https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/skyeng/.env), so you can just run commands below.

- Became SU:
```
sudo su
```

- Run docker-compose:
```
docker-compose up -d --build --force-recreate
```

- Let's go to [Airflow's UI](http://localhost:8080/)


# Exit
- To stop all running containers:
```
docker-compose stop
```
- And remove it all:
```
docker-compose rm
```

# Review
1.
<p align="center">
  <img src="https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/images/datawarehouse.png" width="512" class="center">
</p>

2. 
  I decided to choose the star schema for my datawarehouse because we don't have a lot of different tables in our datasource, so we can describe business logic correctly by linking all entities in one fact table. Also we can scale our datawarehouse by adding more dimension tables and linking them in the fact table. Another one advantage of this scheme is the speed of modeling.
  
3.
   Let me describe few moments. Tasks with `e_` prefix means [extract](https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/skyeng/dags/to_datawarehouse.py#LL10C5-L10C25) task, `t_` means [transform](https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/skyeng/dags/to_datawarehouse.py#LL10C5-L10C25) and `l_` means [load](https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/skyeng/dags/to_datawarehouse.py#LL138C5-L138C18).
<p align="center">
  <img src="https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/images/to_datawarehouse.png" width="1024" class="center">
</p>
  
  - DAG starts by extracting data from datasource (`e_from_pg_datasource`) and datawarehouse (`e_from_pg_datawarehouse`). 
  
  - After that, rows in the both datasets are compared to find new entries (`t_find_new_rows`). But if no entries was found DAG [raise](https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/skyeng/dags/to_datawarehouse.py#L136) `AirflowSkipException` to skip all upstream tasks. We are totally sure that we won't skip any rows updates because we compare two denormalized dataframes. Sometimes duplicates will occurre but we can filter them by `updated_at` columns.
  
  - When we found new entries we should update the hubs entities in datawarehouse (`l_update_hubs`).
  
  - We also should update satellites and links tables in our datawarehouse but we can't do it without hub's primary key and the next task is extracting hub's primary key from datawarehouse (`e_hubs_pk_from_datawarehouse`).
  
  - In the end of the pipeline we updated links (`l_update_links`) and satellites (`l_update_satellites`).
  
  ---
  
But our datamart isn't stored in datawarehouse. For that purposes we use ClickHouse to store all datamarts here.
<p align="center">
  <img src="https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/images/datamart.png" width="256" class="center">
</p>

Entities in the ClickHouse are completely denormalized to avoid joins and get better speed performance. 


So, we have one more DAG to update datamarts.
<p align="center">
  <img src="https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/images/to_datamart.png" width="1024" class="center">
</p>

  - DAG starts by extracting data from datawarehouse (`e_from_pg_datawarehouse`) and datamart (`e_from_ch_datamart`). 
  
  - After that, rows in the both datasets are compared to find new entries (`t_find_new_rows`). 
  
  - When we found new entries we should update datamart (`l_update_datamart`).

---

<p align="center">
  <img src="https://github.com/e183b796621afbf902067460/skyeng-data-engineer/blob/master/images/dag_history.png" width="1024" class="center">
</p>
<p align="center"> DAG History </p>

4.
