# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*'],
 'src': ['static/*', 'static/images/*', 'static/vendor/*', 'templates/*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'cadquery-massembly>=0.9.0,<0.10.0',
 'jupyter-cadquery>=3.2.2,<4.0.0',
 'matplotlib>=3.5.3,<4.0.0']

extras_require = \
{'cadquery': ['cadquery==2.2.0b0', 'casadi==3.5.5']}

entry_points = \
{'console_scripts': ['cq-server = src.cli:main']}

setup_kwargs = {
    'name': 'cadquery-server',
    'version': '0.2',
    'description': 'A web server used to render 3d models from CadQuery code loaded dynamically.',
    'long_description': '# CadQuery server\n\nA web server used to render 3d models from CadQuery code loaded dynamically.\n\nIt has been created for the [Cadquery VSCode extension](https://open-vsx.org/extension/roipoussiere/cadquery), but can be used as standalone.\n\nBecause the CadQuery module is loaded when starting the web server and the scripts are loaded dynamically by request, it has a fast response time.\n\nExample usage in the VSCode extension:\n\n![](./images/screenshot.png)\n\nPlease note that the web server is intended for personal use and it\'s absolutely not safe to open it to a public network.\n\n## Installation\n\n    pip install cq-server\n\n## Usage\n\n### Starting the server\n\nOnce installed, the `cq-server` command should be available on your system:\n\nCLI options:\n\n- `-p`, `--port`: Server port (default: 5000);\n- `-d`, `--dir`: Path of the directory containing CadQuery scripts (default: ".");\n- `-m`, `--module`: Default module (default: "main");\n- `-o`, `--object`: Default rendered object variable name (default: "result");\n- `-f`, `--format`: Default output format (default: "json").\n\nThis list might not be up to date, please use `-h` to list all options.\n\nExample:\n\n    cq-server -p 5000 -d ./examples -m box -o result\n\nThis command will run the server on the port `5000`, load the `box.py` python file in the `./examples` directory and render the CadQuery model named `result`. These two last options can be overridden by url parameters if necessary.\n\n### Writing a CadQuery code\n\nExample:\n\n```py\nimport cadquery as cq\n\nmodel = cq.Workplane("XY").box(1, 2, 3)\n```\n\nPlease read the [CadQuery documentation](https://cadquery.readthedocs.io/en/latest/) for more details about the CadQuery library.\n\n### Using the web server\n\nOnce the server is started, go to its url (ie. `http://127.0.0.1`).\n\nOptional url parameters:\n\n- `module`: name of module to load (default: defined in the `--module` cli option);\n- `object`: variable name of object to render (default: defined in the `--object` cli option).\n\nexample: `http://127.0.0.1?module=box&object=result`).\n\nNote that the `/json` endpoint is used internally and can be used for advanced use. It takes same parameters but returns the model as a threejs json object.\n',
    'author': 'Roipoussiere',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://open-vsx.org/extension/roipoussiere/cadquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
