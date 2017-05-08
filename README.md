# info_service

## Deploy

1. Configure Environment file

**Deploy Environment FILE (container.env)**

```
WEBVIEW_REDIS_HOST=<Docker engine host machine IP>
BROKER_HOST=<usually machine IP>
C_FORCE_ROOT=true
CELERY_ACCEPT_CONTENT=json
```

2. Run

```
docker-compose stop && docker-compose build && dockder-compose up -d && docker-compose ps
```

## Test

1. Configure Environment file

**Test Environment FILE (container.test.env)**

```
WEBVIEW_REDIS_HOST=<Docker engine host machine IP>
```

2. Run

```
./start_test.sh && docker-compose -f docker-compose.test.yml logs --tail="100" info_api_test
```
