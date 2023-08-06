# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmo']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'cosmo',
    'version': '0.3.4',
    'description': 'A web server implementation that uses raw sockets.',
    'long_description': '# Cosmo\n\nCosmo is a multithreaded python webserver that I\'m developing in my spare time. Cosmo utilizes a TCP socket to send and receive data.\n\n## Examples\n\n### Simple Server\n\n```py\nfrom cosmo import App, Request, Response\n\napp = App("0.0.0.0", 8080)\n\n@app.route("/", "text/html")\ndef index(request: Request):\n    return Response(f"<h1>{request.address}</h1>")\n\napp.serve()\n```\n\n### Using Custom Headers\n\n```py\nfrom cosmo import App, Request, Response\n\napp = App("0.0.0.0", 8080)\n\n@app.route("/", "text/html")\ndef index(request: Request):\n    headers = {"x-custom-header": "custom"}\n    content = "<h1>Custom Headers: </h1>\\n<ul>"\n    for header in headers.keys():\n        content += f"<li>{header}: {headers[header]}</li>\\n"\n    content += "</ul>"\n    return Response(content, headers)\n\napp.serve()\n```\n\n### Returning an HTML Page\n\n```py\nfrom cosmo import App, html_page, Request, Response\n\napp = App("0.0.0.0", 8080)\n\n@app.route("/", "text/html")\ndef index(request: Request):\n    return Response(html_page("path/to/page.html"))\n```\n\n## Docs\n\nComing soon...',
    'author': 'Kronifer',
    'author_email': '44979306+Kronifer@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kronifer/cosmo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
