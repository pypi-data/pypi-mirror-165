# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_clients', 'aio_clients.multipart']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0']

setup_kwargs = {
    'name': 'aio-clients',
    'version': '0.1.0b7',
    'description': 'Python aiohttp client',
    'long_description': '# aiohttp client\n\n### What is the difference from aiohttp.Client?\n\nIt is simpler and as a Requests\n\n----\n# Example: \n\n\n## Base reqeust: \n\n```python\nimport asyncio\nfrom aio_clients import Http, Options\n\n\nasync def main():\n    r = await Http().get(\'http://google.com\', o=Options(is_json=False, is_raw=True, is_close_session=True))\n    print(f\'code={r.code} body={r.raw_body}\')\n\n\nasyncio.run(main())\n```\n\n## Async reqeust\n\n```python\nimport asyncio\n\nimport aiohttp\n\nfrom aio_clients import Http, Options\n\n\nasync def on_request_start(session, trace_config_ctx, params):\n    print("Starting request")\n\n\nasync def on_request_end(session, trace_config_ctx, params):\n    print("Ending request")\n\n\nasync def main():\n    trace_config = aiohttp.TraceConfig()\n    trace_config.on_request_start.append(on_request_start)\n    trace_config.on_request_end.append(on_request_end)\n\n    http = Http(\n        host=\'http://google.com/search?q=\',\n        trace_config=trace_config\n    )\n\n    r = await asyncio.gather(\n        http.get(\'test\', o=Options(is_json=False, is_raw=True)),\n        http.get(\'hello world\', o=Options(is_json=False, is_raw=True)),\n        http.get(\'ping\', o=Options(is_json=False, is_raw=True)),\n    )\n\n    print(f\'status code={[i.code for i in r]}\')\n    await http.close()\n\n\nasyncio.run(main())\n```\n',
    'author': 'Denis Malin',
    'author_email': 'denis@malina.page',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skar404/aio-clients',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
