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
