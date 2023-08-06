# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cq_server']

package_data = \
{'': ['*'],
 'cq_server': ['static/*', 'static/images/*', 'static/vendor/*', 'templates/*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'cadquery-massembly>=0.9.0,<0.10.0',
 'jupyter-cadquery>=3.2.2,<4.0.0',
 'matplotlib>=3.5.3,<4.0.0']

extras_require = \
{'cadquery': ['cadquery==2.2.0b0', 'casadi==3.5.5']}

entry_points = \
{'console_scripts': ['cq-server = cq_server.cli:main']}

setup_kwargs = {
    'name': 'cadquery-server',
    'version': '0.2.2',
    'description': 'A web server used to render 3d models from CadQuery code loaded dynamically.',
    'long_description': '# CadQuery server\n\nA web server used to render 3d models from CadQuery code loaded dynamically.\n\nIt has been created for the [Cadquery VSCode extension](https://open-vsx.org/extension/roipoussiere/cadquery), but can be used as standalone.\n\nExample usage with Kate on the left and Firefox on the right:\n\n![](./images/screenshot.png)\n\n## Features\n\n- fast response time\n- built-in file-watcher\n- live-reload\n- use your favorite text editor or IDE\n- display model on an external monitor or other device\n- compatible with VSCode built-in browser\n\nPlease note that the web server is intended for personal use and it\'s absolutely not safe to open it to a public network.\n\n## Functionning\n\nCadQuery Server dynamically loads your CadQuery code and renders the model on the browser using [three-cad-viewer](https://github.com/bernhard-42/three-cad-viewer) (the same used in [jupyter-cadquery](https://github.com/bernhard-42/jupyter-cadquery)). It includes a file watcher that reloads the Python code and updates the web page when the file is updated.\n\nThis approach allows users to work on any IDE, and render the model on any web browser. It also allow them to display the model in an other monitor, or even in an other computer on the same local network (for instance a tablet on your desktop).\n\nThe project was originally started for the VSCode extension, but since it doesn\'t depend on VSCode anymore, it\'s now a project as it own.\n\n## Installation\n\nIf you already have CadQuery installed on your system:\n\n    pip install cadquery-server\n\nIf you want to install both cq-server and CadQuery:\n\n    pip install \'cadquery-server[cadquery]\'\n\nThis may take a while.\n\n## Usage\n\n### Starting the server\n\nOnce installed, the `cq-server` command should be available on your system.\n\nUse `cq-server -h` to list all available options.\n\nPositional arguments:\n\n- `dir`: Path of the directory containing CadQuery scripts (default: ".").\n\nMain options:\n\n- `-p`, `--port`: Server port (default: 5000);\n- `-m`, `--module`: Default module to load (default: "main").\n\nExample:\n\n    cq-server ./examples -p 5000 -m box\n\nThis command will run the server on the port `5000` and load the `box.py` python file in the `./examples` directory. Note that the `-m` option can be overridden by url parameter if necessary (see below).\n\n### UI cli options\n\nOther cli options are available to change the UI appearence:\n\n- `--ui-hide`: a comma-separated list of buttons to disable, among: `axes`, `axes0`, `grid`, `ortho`, `more`, `help`;\n- `--ui-glass`: activate tree view glass mode;\n- `--ui-theme`: set ui theme, `light` or `dark` (default: browser config);\n- `--ui-trackball`: set control mode to trackball instead orbit;\n- `--ui-perspective`: set camera view to perspective instead orthogonal;\n- `--ui-grid`: display a grid in specified axes (`x`, `y`, `z`, `xy`, etc.);\n- `--ui-transparent`: make objects semi-transparent;\n- `--ui-black-edges`: make edges black.\n\nExample:\n\n    cq-server --ui-hide ortho,more,help --ui-glass --ui-theme light --ui-grid xyz\n\n### Writing a CadQuery code\n\nCadQuery Server renders the model defined in the `show_object()` function (like in CadQuery Editor).\n\nYou **must** import it before from the `cq_server.ui` module, among with the `UI` class, which is used by the server to load the model.\n\nMinimal working example:\n\n```py\nimport cadquery as cq\nfrom cq_server.ui import UI, show_object\n\nshow_object(cq.Workplane(\'XY\').box(1, 2, 3))\n```\n\nPlease read the [CadQuery documentation](https://cadquery.readthedocs.io/en/latest/) for more details about the CadQuery library.\n\n### Using the web server\n\nOnce the server is started, go to its url (ie. `http://127.0.0.1`).\n\nOptional url parameters:\n\n- `module`: name of module to load (default: defined in the `--module` cli option);\n\nexample: `http://127.0.0.1?module=box`).\n\nNote that the `/json` endpoint is used internally and can be used for advanced use. It takes same parameters but returns the model as a threejs json object.\n\nIn VSCode, the web page can be displayed within the IDE using LivePreview extension (ctrl+shift+P -> Simple Browser: Show). This way you can use VSCode debugging tools.\n',
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
