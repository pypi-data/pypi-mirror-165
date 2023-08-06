# **mPyLogs**

## Install
___
```bash
$ pip install -i https://test.pypi.org/simple/ mpylogs
```

## Configure
___

```python
# main.py

from mpylogs.functions import setup_logger

logger = setup_logger()           
logger.http("Uma mensagem http qualquer", { "status": 200, "data": { "message": "Tudo certo por aqui :D" } })
```

> [  HTTP  ] | [STATUSCODE 200] | 2022-08-30 22:48:47 | Uma mensagem http qualquer  | {"message": "Tudo certo por aqui :D"}


## Log Types
___

| Tipo      | Description                                                        |
|-----------|--------------------------------------------------------------------|
| `error`   | Informar exceptions tratadas                                       |
| `warning` | Informar eventos ou estados potencialmente prejudicias ao programa |
| `debug`   | IAcompnhar eventos ou estados do programa                          |
| `info`    | Descrever infos detalhadas sobre o estado do programa              |
| `http`    | Informar dados de requests e responses feitas via http             |


## Middlewares
___

### django
```python
# httpLogger.py

from mpylogs.functions import setup_logger
from django.utils.deprecation import MiddlewareMixin


class HTTPLoggerMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        logger = setup_logger()
        logger.http(f'{request.META.get("REMOTE_ADDR")} {request.method} {request.META.get("PATH_INFO")}', {"status": response.status_code})

        return response

```

```python
# setting.py

MIDDLEWARE = [
    ...,
    'app.utils.httpLogger.HTTPLoggerMiddleware' # path to your middleware file
]

```

### Flask

```python

# Your app setup file
from flask import Flask, request, Response
from mpylogs.functions import setup_logger

app = Flask(__name__)
logger = setup_logger()

@app.after_request
def log_response(response: Response):
    logger.http(f'{request.remote_addr} {request.method} {request.path}', {
                "status": response.status_code})
    return response

```

## Results 
![img.png](img.png)