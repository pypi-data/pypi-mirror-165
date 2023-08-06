# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyvalve']

package_data = \
{'': ['*']}

install_requires = \
['aiofile>=3.8.1,<4.0.0', 'aiopathlib>=0.5.0,<0.6.0', 'asyncinit>=0.2.4,<0.3.0']

setup_kwargs = {
    'name': 'pyvalve',
    'version': '0.1.3',
    'description': 'Asyncio python clamav client',
    'long_description': '# pyvalve\nAsyncio python clamav client library\n\n\n## Usage Examples\n\nPing\n```\npvs = await PyvalveNetwork()\nresponse = await pvs.ping()\n```\nClamAv will respond with "PONG"\n\nScanning\n\n```\npvs = await PyvalveNetwork()\nresponse = await pvs.scan(path)\n```\n\nStream Scanning\n```\nfrom io import BytesIO\nfrom aiofile import AIOFile\n\nbuffer = BytesIO()\nasync with AIOFile(\'some/file\', \'r\') as file_pointer:\n    line = await file_pointer.read_bytes()\n    buffer.write(line)\n    buffer.seek(0)\nresponse = await pvs.instream(buffer)\n```\n\n## Documentation\n\n### _class_ Pyvalve()\nBases: `object`\n\nPyvalve base class\n\n#### set_persistant_connection(persist)\nSet persistent connection\n\n\n* **Parameters**\n\n    **bool** (*persist*) – persistent connection True/False\n\n\n\n* **Return type**\n\n    `None`\n\n\n\n#### set_stream_buffer(length)\nSet stream buffer\n\n\n* **Parameters**\n\n    **int** (*length*) – Desired stream buffer in bytes\n\n\n\n* **Return type**\n\n    `None`\n\n\n#### _async_ allmatchscan(path)\nSend allmatchscan command\n\n\n* **Parameters**\n\n    **str** (*path*) – Path to file/directory to be scanned\n\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n\n* **Raises**\n\n    **PyvalveScanningError** – If path is not found\n\n\n\n#### _async_ contscan(path)\nSend constscan command\n\n\n* **Parameters**\n\n    **str** (*path*) – Path to file/directory to be scanned\n\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n\n* **Raises**\n\n    **PyvalveScanningError** – If path is not found\n\n\n#### _async_ instream(buffer)\nSend a stream to clamav\n\n\n* **Parameters**\n\n    **buffer** (*BinaryIO*) – a buffer object\n\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n\n* **Raises**\n\n    \n    * **PyvalveConnectionError** – If connection is broken\n\n\n    * **PyvalveStreamMaxLength** – If stream size limit exceeded\n\n\n\n#### _async_ multiscan(path)\nSend multiscan command\n\n\n* **Parameters**\n\n    **str** (*path*) – Path to file/directory to be scanned\n\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n\n* **Raises**\n\n    **PyvalveScanningError** – If path is not found\n\n\n\n#### _async_ ping()\nSend ping command\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n\n#### _async_ reload()\nSend reload command\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n\n#### _async_ scan(path)\nSend scan command\n\n\n* **Parameters**\n\n    **str** (*path*) – Path to file/directory to be scanned\n\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n\n* **Raises**\n\n    **PyvalveScanningError** – If path is not found\n\n\n\n#### _async_ shutdown()\nSend shutdown command\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n#### _async_ stats()\nSend stats command\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n\n#### _async_ version()\nSend version command\n\n\n* **Returns**\n\n    Response from clamav\n\n\n\n* **Return type**\n\n    str\n\n\n### _class_ PyvalveNetwork(host=\'localhost\', port=3310, timeout=None)\nBases: `Pyvalve`\n\nAsyncio Clamd network client\n\n\n#### _async_ \\__init__(host=\'localhost\', port=3310, timeout=None)\nPyvalveNetwork Constructor\n\n\n* **Parameters**\n\n    \n    * **str** (*host*) – host address for clamav\n\n\n    * **int** (*timeout*) – listening port for clamav\n\n\n    * **int** – socket timemout\n\n\n### _class_ PyvalveSocket(socket=\'/tmp/clamd.socket\', timeout=None)\nBases: `Pyvalve`\n\nAsyncio Clamd socket client\n\n\n#### _async_ \\__init__(socket=\'/tmp/clamd.socket\', timeout=None)\nPyvalveSocket Constructor\n\n\n* **Parameters**\n\n    \n    * **str** (*socket*) – Path to socket file\n\n\n    * **int** (*timeout*) – socket timemout\n\n\n\n## Exceptions\n\n### _exception_ PyvalveError()\nBases: `Exception`\n\nPyvalve exception base class\n\n### _exception_ PyvalveConnectionError()\nBases: `PyvalveError`\n\nException communicating with clamd\n\n### _exception_ PyvalveResponseError()\nBases: `PyvalveError`\n\nException processing response\n\n### _exception_ PyvalveScanningError()\nBases: `PyvalveError`\n\nException scanning. Could be path not found.\n\n### _exception_ PyvalveStreamMaxLength()\nBases: `PyvalveResponseError`\n\nException using INSTREAM with a buffer\nlength > StreamMaxLength in /etc/clamav/clamd.conf\n',
    'author': 'Bradley Sacks',
    'author_email': 'bradsacks99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bradsacks99/pyvalve',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
