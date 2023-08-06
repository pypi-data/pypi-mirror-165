# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cnext_server',
 'cnext_server.server',
 'cnext_server.server.python',
 'cnext_server.server.python.cassist',
 'cnext_server.server.python.code_editor',
 'cnext_server.server.python.dataframe_manager',
 'cnext_server.server.python.executor_manager',
 'cnext_server.server.python.experiment_manager',
 'cnext_server.server.python.file_explorer',
 'cnext_server.server.python.file_manager',
 'cnext_server.server.python.jupyter_server_manager',
 'cnext_server.server.python.libs',
 'cnext_server.server.python.logs_manager',
 'cnext_server.server.python.model_manager',
 'cnext_server.server.python.project_manager',
 'cnext_server.server.python.user_space',
 'cnext_server.server.python.user_space.ipython',
 'cnext_server.server.tests',
 'cnext_server.server.tests.test_servers']

package_data = \
{'': ['*'],
 'cnext_server': ['public/*',
                  'public/_next/static/BzracgFIE9T4HuB0KTAH5/*',
                  'public/_next/static/chunks/*',
                  'public/_next/static/chunks/pages/*',
                  'public/_next/static/css/*',
                  'public/icons/*'],
 'cnext_server.server': ['build/*', 'ls/*', 'routes/*']}

install_requires = \
['cnextlib>=0.5.0,<0.6.0',
 'jupyter-client>=7.2.2,<7.3.0',
 'jupyter-resource-usage>=0.6.1,<0.7.0',
 'jupyterlab>=3.3.4,<3.4.0',
 'matplotlib>=3.5.1,<3.6.0',
 'mlflow>=1.25.1,<2.0.0',
 'multipledispatch>=0.6.0,<0.7.0',
 'netron>=5.7.8,<6.0.0',
 'pandas>=1.3.5,<1.4.0',
 'plotly>=5.7.0,<5.8.0',
 'protobuf==3.20.1',
 'pyreadline>=2.1,<3.0',
 'python-language-server>=0.36.2,<0.37.0',
 'pyyaml>=5.1,<6.0',
 'pyzmq>=23.2.0,<24.0.0',
 'requests>=2.27.1,<3.0.0',
 'send2trash>=1.8.0,<2.0.0',
 'sentry-sdk>=1.5.12,<2.0.0',
 'simplejson>=3.17.6,<4.0.0']

entry_points = \
{'console_scripts': ['cnext-init = cnext_server.__main__:main',
                     'cnext-path = cnext_server.__main__:path',
                     'cnext-run = cnext_server.__main__:start']}

setup_kwargs = {
    'name': 'cnext',
    'version': '0.6.0',
    'description': 'The data-centric workspace for AI & DS',
    'long_description': '# CNext Instructions\n\n[Website] - [Documentation] - [Docker Image] - [Overview Video]\n\n## Setup and run the CNext workspace\n\nCNext is a data-centric workspace for DS and AI. Our workspace is meant to consolidate the most common tasks performed by data scientists and ML engineers. At a high level our workspace allows for:\n\n-   Data exploration & transformation\n-   Model development / exploration\n-   Production code generation\n-   Dashboard & App Generation\n-   Experiment Management\n\n## Features\n\n-   Interactive Python coding envrionment with native Python output (think Jupyter replacement)\n-   Smart code suggestion (categorical values and column names)\n-   Interactive data exploration\n-   Automative visualizations\n-   Experiment and model management\n-   Instant dashboarding\n\n## Installation via Docker\n\ncnext is also available via pre-built Docker images. To get started, you can simply run the following command:\n\n```bash\ndocker run --rm -it -p 4000:4000 -p 5000:5000 -p 5011:5011 -p 5008:5008 -p 5005:5005 cycai/cnext\n```\n\nThe web application will launch at: `http://localhost:4000` or `http://127.0.0.1:4000/`\n\n## Installation via Pip\n\nPLEASE NOTE: CNext requires npm >= 18.4 and Python >= 3.9.7 . Please ensure your environment meets the minimum requirements before beginning the installation. \n\nStep 1: Make sure `Nodejs` is available in your computer (try `npm --version` and make sure it work)\n\nStep 2: `run` command `pip install cnext`\n\nStep 3: `run` command `cnext-init`\n\n-   Input `Enter path to the cnext sample project created in Step 1` and hit `Enter` (Example `C:/Skywalker`)\n    \u200b\n\nStep 4 `run` command `cnext-run`\n\n-   Web application will launch at : `http://localhost:CLIENT_PORT` or `http://127.0.0.1:CLIENT_PORT/` (CLIENT_PORT default is 4000)\n-   Stop application: `Ctrl + c | Command + c`\n-   Note: Pay attention at `CLIENT_PORT`, and `SERVER_PORT` in `.env` file (you will have to change these ports if you already use them on your machine)\n\n\n## License\n\nCopyright 2022 CycAI Inc.\n\u200b\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\u200b\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\u200b\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n[website]: https://www.cnext.io/\n[docker image]: https://hub.docker.com/r/cycai/cnext\n[documentation]: https://docs.cnext.io/\n[overview video]: https://youtu.be/5eWPkQIUfZw\n[cnext]: https://drive.google.com/file/d/1ft4PmFclylOtEAQSPBqn9nUSyAkMs5R-\n[docker]: https://www.docker.com/products/docker-desktop/\n',
    'author': 'CycAI Inc',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cyc-ai.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
