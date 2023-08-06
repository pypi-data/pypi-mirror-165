<h1>Simple API Framework</h1>

This framework is based on Tornado, and it's used to simplify the development of small microservices.

To install it, just get the latest version from PyPi:

```shell
pip install simple-api-framework
```

To start you'll need to do this steps:

- Create an `.env` file and put this environment variables:

```shell
ENV=local
API_VERSION=1
SERVICE_HOST=127.0.0.1
SERVICE_PORT=50000

CORS_ENABLED=1
CORS_ALLOWED_ORIGINS=*

REDIS_URL=
REDIS_PREFIX=

MONGODB_URL=

DB_URL=
DB_TIMEOUT=15
DB_RESULTS_LIMIT=20
```

- Create a `run.py`:

```python
from simple_api_framework import Service, Endpoint


class TestEndpoint(Endpoint):
    methods = ['GET']
    
    async def get(self, *args, **kwargs):
        self.finish_with_ok_status()


class MyService(Service):
    NAME = 'service'

    def __init__(self):
        urls = [
            {'url': 'test', 'handler': TestEndpoint}
        ]
        super().__init__(urls=urls)


if __name__ == '__main__':
    MyService()

```

- Run this file and test `http://127.0.0.1:50000/api/v1/test/` endpoint - it should return you HTTP 200 status and 
response:

```json
{
  "ok": true
}
```
