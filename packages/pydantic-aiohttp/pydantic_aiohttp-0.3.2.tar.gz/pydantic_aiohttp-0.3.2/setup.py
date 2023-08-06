# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_aiohttp']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiohttp[speedups]>=3.8.1,<4.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'ujson>=5.4.0,<6.0.0']

setup_kwargs = {
    'name': 'pydantic-aiohttp',
    'version': '0.3.2',
    'description': 'Simple HTTP Client based on aiohttp with integration of pydantic',
    'long_description': '# pydantic_aiohttp - Symbiosis of [Pydantic](https://github.com/samuelcolvin/pydantic) and [Aiohttp](https://github.com/aio-libs/aiohttp)\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)\n[![PyPI license](https://img.shields.io/pypi/l/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)\n\nThis repository provides simple HTTP Client based on aiohttp with integration of pydantic\n\n## Examples\n\n### Basic example\n\n```python\nimport asyncio\n\nimport pydantic\n\nfrom pydantic_aiohttp import Client\n\n\nclass HelloWorldResponse(pydantic.BaseModel):\n    hello: str\n\n\nasync def main():\n    example_client = Client("https://api.example.com")\n\n    response = await example_client.get("/hello", response_model=HelloWorldResponse)\n    print(response.hello)\n\n    # After all your work is done you should close client (this method closes aiohttp session instance)\n    await example_client.close()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n\n```\n\n### Use as context manager\n\n```python\nimport asyncio\n\nimport pydantic\n\nfrom pydantic_aiohttp import Client\n\n\nclass HelloWorldResponse(pydantic.BaseModel):\n    hello: str\n\n\nasync def main():\n    # Client will be closed automatically on exit from context\n    async with Client("https://api.example.com") as client:\n        response = await client.get("/hello", response_model=HelloWorldResponse)\n    \n    print(response.hello)\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n\n```\n\n### Handling errors parsed as pydantic models\n\n```python\nimport http\nimport asyncio\n\nimport pydantic\n\nimport pydantic_aiohttp\nfrom pydantic_aiohttp import Client\n\n\nclass FastAPIValidationError(pydantic.BaseModel):\n    loc: list[str]\n    msg: str\n    type: str\n\n\nclass FastAPIUnprocessableEntityError(pydantic.BaseModel):\n    detail: list[FastAPIValidationError]\n\n\nclass User(pydantic.BaseModel):\n    id: str\n    email: str\n    first_name: str\n    last_name: str\n    is_admin: bool\n\n\nasync def main():\n    client = Client(\n        "https://fastapi.example.com",\n        error_response_models={\n            http.HTTPStatus.UNPROCESSABLE_ENTITY: FastAPIUnprocessableEntityError\n        }\n    )\n\n    try:\n        # Imagine, that "email" field is required for this route\n        await client.post(\n            "/users",\n            body={\n                "first_name": "John",\n                "last_name": "Doe"\n            },\n            response_model=User\n        )\n    except pydantic_aiohttp.HTTPUnprocessableEntity as e:\n        # response field of exception now contain parsed pydantic model entity \n        print(e.response.detail[0].json(indent=4))\n        # >>>\n        # {\n        #     "loc": [\n        #         "body",\n        #         "email"\n        #     ],\n        #     "msg": "field required",\n        #     "type": "value_error.missing"\n        # }\n    finally:\n        await client.close()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n\n```\n\n### Downloading files\n```python\nimport asyncio\n\nfrom pydantic_aiohttp import Client\n\n\nasync def main():\n    client = Client(\'https://source.unsplash.com\')\n\n    try:\n        await client.download_file("/random", filepath="random.jpg")\n    finally:\n        await client.close()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n\n```\n\n## LICENSE\n\nThis project is licensed under the terms of the [MIT](https://github.com/pylakey/aiotdlib/blob/master/LICENSE) license.\n',
    'author': 'pylakey',
    'author_email': 'pylakey@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pylakey/pydantic_aiohttp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
