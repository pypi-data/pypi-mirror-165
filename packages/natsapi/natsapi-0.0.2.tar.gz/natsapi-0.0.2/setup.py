# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['natsapi', 'natsapi.asyncapi', 'natsapi.client']

package_data = \
{'': ['*']}

install_requires = \
['nats-py[nkeys]>=2.1.0,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'watchgod>=0.8.2,<0.9.0']

entry_points = \
{'pytest11': ['natsapi = natsapi.plugin']}

setup_kwargs = {
    'name': 'natsapi',
    'version': '0.0.2',
    'description': 'An opinionated wrapper for the NATS client with spec generation capability',
    'long_description': '# NatsAPI\n\n## Table of Contents\n\n<!-- vim-markdown-toc GitLab -->\n\n* [Installation](#installation)\n* [Usage](#usage)\n    * [Docs](#docs)\n    * [Examples](#examples)\n        * [Basic](#basic)\n        * [Error handling with sentry](#error-handling-with-sentry)\n        * [Reload](#reload)\n    * [Generating documentation (asyncapi)](#generating-documentation-asyncapi)\n    * [Plugins](#plugins)\n* [History](#history)\n\n<!-- vim-markdown-toc -->\n\nNatsAPI is a framework to develop Python3 applications that uses [nats](https://nats.io) as communication medium instead of http. With nats you have a smaller footprint, faster req/s, pub/sub and better observability.\nIt is highly inspired by [FastAPI](https://github.com/tiangolo/fastapi) and has the same development style. NatsAPI produces an [AsyncAPI](https://www.asyncapi.com/) schema out of the box, **this schema is not fully compatible with the standard**.\n\n## Installation\n\n```\n$ pip install natsapi\n```\n\n## Usage\n\n### Docs\n\n> UNDER CONSTRUCTION\n\n### Examples\n\n#### Basic\n\n```python\nfrom natsapi import NatsAPI, SubjectRouter\nfrom pydantic import BaseModel\n\n\nclass Message(BaseModel):\n    message: str\n\n\nclass Person(BaseModel):\n    first_name: str\n    last_name: str\n\n\napp = NatsAPI("natsapi")\nrouter = SubjectRouter()\n\n\n@router.request("persons.greet", result=Message)\nasync def greet_person(app: NatsAPI, person: Person):\n    return {"message": f"Greetings {person.first_name} {person.last_name}!"}\n\n\napp.include_router(router)\n\nif __name__ == "__main__":\n    app.run()\n```\n\nRun as follows:\n\n```bash\n$ python app.py\n```\n\nWhen sending a request\n\n```shell\n$ nats request natsapi.persons.greet \'{"params": {"person": {"first_name": "Foo", "last_name": "Bar"}}}\'                                                                                                    \n```\n\nYou should see a response like:\n\n```\n18:19:00 Sending request on "natsapi.persons.greet"\n18:19:00 Received on "_INBOX.dpBgTyG9XC5NhagdqRHTcp.eMkVkru8" rtt 1.052463ms\n{"jsonrpc": "2.0", "id": "c2bc2d20-dbd5-4e39-a22d-c22a8631c5a3", "result": {"message": "Greetings Foo Bar!"}, "error": null}\n```\n\n#### Error handling with sentry\n\n\n```python\nfrom natsapi import NatsAPI, SubjectRouter\nimport logging\nfrom pydantic import ValidationError\nfrom sentry_sdk import configure_scope\nfrom natsapi.models import JsonRPCRequest, JsonRPCError\nfrom pydantic import BaseModel\n\n\nclass StatusResult(BaseModel):\n    status: str\n\n\napp = NatsAPI("natsapi-example")\n\nrouter = SubjectRouter()\n\n\n@router.request("healthz", result=StatusResult)\nasync def handle_user(app: NatsAPI):\n    return {"status": "OK"}\n\n\napp.include_router(router)\n\n\ndef configure_sentry(auth):\n    with configure_scope() as scope:\n        scope.user = {\n            "email": auth.get("email"),\n            "id": auth.get("uid"),\n            "ip_address": auth.get("ip_address"),\n        }\n\n\n@app.exception_handler(ValidationError)\nasync def handle_validation_exception(exc: ValidationError, request: JsonRPCRequest, subject: str) -> JsonRPCError:\n    auth = request.params.get("auth") or {}\n    configure_sentry(auth)\n    logging.error(\n        exc,\n        exc_info=True,\n        stack_info=True,\n        extra={"auth": auth, "json": request.dict(), "subject": subject, "NATS": True, "code": -32003},\n    )\n\n    return JsonRPCError(code=-90001, message="VALIDATION_ERROR", data={"error_str": str(exc)})\n\n\nif __name__ == "__main__":\n    app.run(reload=False)\n```\n\n#### Reload\n\nWhen running from a file you can add a reload flag (hot-reload on file change) or use the `NATSAPI_RELOAD` env var.\n\n```\nif __name__ == "__main__":\n    app.run(reload=True)\n```\n\n### Generating documentation (asyncapi)\n\nTo see the documentation, you can use the binary to run the server. Root path is `natsapi-example` so:\n\n```bash\n$ ./nats-redoc 4222 master.trinity-testing\n\nServer running\nDocs can be found on localhost:8090\nconnected to nats on port 4222\n```\n\nWhen surfing to [localhost:8090](http://127.0.0.1:8090), the documentation should look like this:\n\n![Example of redoc](./doc/readme-example-redoc.png)\n\n### Plugins\n\nPlugins can be added and are found in `natsapi/plugin.py`.\n\n- [natsapi_mock](./natsapi/plugin.py): A handy mock fixture to intercept nats requests and to fake nats responses for any subject.\n\n## History\n\nNatsapi is the first opensource framework build by WeGroup. The project started as an intern assignment led by @sevaho and developed by @fversche and @mark-yousif.\n',
    'author': 'WeGroup NV',
    'author_email': 'it@wegroup.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wegroupwolves/natsapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
