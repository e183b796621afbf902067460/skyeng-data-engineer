# C3D3 Dagster
Depends on: [raffaelo](https://github.com/e183b796621afbf902067460/raffaelo) and [medici](https://github.com/e183b796621afbf902067460/medici), [d3f1nance](https://github.com/e183b796621afbf902067460/d3f1nance) and [c3f1nance](https://github.com/e183b796621afbf902067460/c3f1nance), [d3tl](https://github.com/e183b796621afbf902067460/d3tl) and [c3tl](https://github.com/e183b796621afbf902067460/c3tl).

---

Dagster is used for C3D3 ETL orchestration.

# Configuration

- Clone current repository:
```
git clone https://github.com/e183b796621afbf902067460/c3d3-dagster.git
```

- Get into the project folder:
```
cd c3d3-dagster/c3d3
```

- Set environment variables in [.env](https://github.com/e183b796621afbf902067460/c3d3-dagster/blob/master/c3d3/.env).

# Docker

- Run docker compose (`sudo`):
```
docker-compose up -d --build
```

# Exit
- To stop all running containers:
```
docker stop $(docker ps -a -q)
```
- And remove it all:
```
docker rm $(docker ps -a -q)
```
