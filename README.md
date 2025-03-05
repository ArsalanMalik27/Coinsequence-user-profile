copy `.env.example` to `.env`

Run project locally
`docker compose -f docker/docker-compose.local.yml up --build --force-recreate`

Add deps
`poetry add <dep_name>`

Run auto migration from schema
run project locally, in another tab
`docker ps -a`
`docker exec -it <container_id> /bin/bash`
`alembic revision --autogenerate -m "<commit message>"`

Enabling GCP cloud artifacts
`gcloud config set artifacts/repository cs-packages`
`gcloud config set artifacts/location us-east4`
`gcloud config set account artifact-owner@dev-antonym-320118.iam.gserviceaccount.com`


`export GCP_ACCESS_TOKEN="$(gcloud auth print-access-token)"`

### Run local
copy `.env.example` to `.env`  
`docker compose -f docker/docker-compose.local.yml up --build --force-recreate`  

you will be able access Swagger docs at `http://localhost:8000/docs#/`  
And database at `http://localhost:8080/` - Please refer to `docker-compose.local.yml` for DB environment details
