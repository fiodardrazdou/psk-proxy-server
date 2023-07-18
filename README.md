# Python Proxy Server
## Description
This project is a Python Proxy Storage Server, designed to store, manage, and provide proxies 
upon request. Clients can add, edit, and retrieve proxies through dedicated endpoints.

## Features
- Store proxies with various attributes.
- Rotate and return N proxies by calling the /proxy/generate endpoint.
- Add new proxies using the POST endpoint.
- Edit existing proxies using the PUT endpoint.
- Fetch stored proxies by id using the GET endpoint.

## Installation
This project requires Python 3.10 or newer.

1. Clone the repository:
``` bash
git clone https://github.com/fiodardrazdou/psk-proxy-server.git
```
2. Navigate to the project directory:
``` bash
cd psk-proxy-server
```
3. Install the necessary dependencies:
``` bash
poetry install
```
4. Run the migrations:
``` bash
source .env.local
poetry run alembic upgrade head
```

## Usage
Run locally
``` bash
source .env.local
cd app
poetry run uvicorn app.main:app --host 0.0.0.0 --forwarded-allow-ips='*'
```
or run docker container
``` bash
docker-compose build
docker-compose up
```

## Testing
Run auto tests'
``` bash
source .env.local
python -m unittest tests.automation.test_main
```

# API Endpoints
## GET /proxy/generate
### Description
Returns N proxies from the database, rotating the proxies in the database if necessary.
### Parameters
- **count** - number of proxies to return
- **job_name** - name of the job that is requesting the proxies
- **proxy_type** - type of proxies to return
## POST /proxy
### Description
Adds a new proxy to the database.
### Parameters
- **ip** - IP address of the proxy
- **port** - port of the proxy
- **username** - username of the proxy
- **password** - password of the proxy
- **proxy_type** - type of the proxy
- **country** - country of the proxy
- **service_name** - name of the service that the proxy is used for
- **job_names** - list of jobs that the proxy is used for
- **active** - whether the proxy is active or not
## PUT /proxy/{proxy_id}
### Description
Edits an existing proxy in the database.
### Parameters
- **proxy_id** - id of the proxy to edit
- **port** - port of the proxy
- **username** - username of the proxy
- **password** - password of the proxy
- **proxy_type** - type of the proxy
- **job_names** - list of jobs that the proxy is used for
- **active** - whether the proxy is active or not
## GET /proxy/{proxy_id}
### Description
Returns a proxy from the database by id.
### Parameters
- **proxy_id** - id of the proxy to return
## GET /proxies
### Description
Returns all proxies from the database.
### Parameters
- **job_name** - name of the job that is requesting the proxies
- **proxy_type** - type of proxies to return
- **page_offset** - offset of the page to return
- **page_limit** - limit of the page to return