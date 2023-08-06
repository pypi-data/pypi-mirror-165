# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['euporie',
 'euporie.console',
 'euporie.console.tabs',
 'euporie.core',
 'euporie.core.comm',
 'euporie.core.convert',
 'euporie.core.convert.formats',
 'euporie.core.formatted_text',
 'euporie.core.key_binding',
 'euporie.core.key_binding.bindings',
 'euporie.core.tabs',
 'euporie.core.widgets',
 'euporie.hub',
 'euporie.notebook',
 'euporie.notebook.tabs',
 'euporie.preview',
 'euporie.preview.tabs']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0,<10.0',
 'Pygments>=2.11.2,<3.0.0',
 'aenum>=3.1,<4.0',
 'appdirs>=1.4,<2.0',
 'fastjsonschema>=2.15.3,<3.0.0',
 'flatlatex>=0.15,<0.16',
 'imagesize>=1.3.0,<2.0.0',
 'jupyter-client>=7.1,<8.0',
 'linkify>=1.4,<2.0',
 'markdown-it-py[linkify]>=2.0.1,<3.0.0',
 'mdit-py-plugins>=0.3.0,<0.4.0',
 'nbformat>=5,<6',
 'prompt-toolkit>=3.0.27,<4.0.0',
 'pyperclip>=1.8,<2.0',
 'timg>=1.1,<2.0',
 'typing-extensions>=4.2.0,<5.0.0',
 'universal-pathlib>=0.0.19,<0.0.20']

extras_require = \
{'all': ['asyncssh>=2.10.1,<3.0.0',
         'black>=19.3b0',
         'isort>=5.10.1,<6.0.0',
         'ssort>=0.11.6,<0.12.0',
         'CairoSVG>=2.5,<3.0'],
 'formatters': ['black>=19.3b0',
                'isort>=5.10.1,<6.0.0',
                'ssort>=0.11.6,<0.12.0'],
 'html-mtable': ['mtable>=0.1,<0.2', 'html5lib>=1.1,<2.0'],
 'hub': ['asyncssh>=2.10.1,<3.0.0'],
 'images-img2unicode': ['img2unicode>=0.1a8,<0.2'],
 'latex-sympy': ['sympy>=1.9,<2.0', 'antlr4-python3-runtime>=4.9,<5.0'],
 'svg-cairosvg': ['CairoSVG>=2.5,<3.0']}

entry_points = \
{'console_scripts': ['euporie = euporie.core.__main__:main',
                     'euporie-console = euporie.console.__main__:main',
                     'euporie-hub = euporie.hub.__main__:main',
                     'euporie-notebook = euporie.notebook.__main__:main',
                     'euporie-preview = euporie.preview.__main__:main'],
 'euporie.apps': ['console = euporie.console.app:ConsoleApp',
                  'hub = euporie.hub.app:HubApp',
                  'launch = euporie.core.launch:CoreApp',
                  'notebook = euporie.notebook.app:NotebookApp',
                  'preview = euporie.preview.app:PreviewApp'],
 'pygments.lexers': ['argparse = euporie.core.pygments:ArgparseLexer'],
 'pygments.styles': ['euporie = euporie.core.pygments:EuporiePygmentsStyle']}

setup_kwargs = {
    'name': 'euporie',
    'version': '2.0.4',
    'description': 'Euporie is a suite of terminal applications for interacting with Jupyter kernels',
    'long_description': '|logo|\n\n.. |logo| image:: https://user-images.githubusercontent.com/12154190/160670889-c6fc4cd8-413d-49f0-b105-9c0e03117032.svg\n   :alt: <Logo>\n\n#######\neuporie\n#######\n\n|PyPI| |RTD| |PyVer| |License| |Binder| |Stars|\n\n.. content_start\n\n**Euporie is a terminal based interactive computing environment for Jupyter.**\n\nEuporie\'s apps allow you to interact with Jupyter kernels, and run Jupyter notebooks - entirely from the terminal.\n\n.. list-table::\n   :align: center\n   :widths: 25 25 25 25\n   :class: text-center\n\n   * - `Console <https://euporie.readthedocs.io/en/latest/apps/console.html>`_\n     - `Notebook <https://euporie.readthedocs.io/en/latest/apps/notebook.html>`_\n     - `Preview <https://euporie.readthedocs.io/en/latest/apps/preview.html>`_\n     - `Hub <https://euporie.readthedocs.io/en/latest/apps/hub.html>`_\n\n.. image:: https://user-images.githubusercontent.com/12154190/182201621-9c3e4b04-1b1e-46e3-b852-b43f16adfc7b.png\n   :target: https://user-images.githubusercontent.com/12154190/182201621-9c3e4b04-1b1e-46e3-b852-b43f16adfc7b.png\n\n`View more screenshots here <https://euporie.readthedocs.io/en/latest/pages/gallery.html>`_\n\n----\n\n*******\nInstall\n*******\n\nYou can install euporie with `pipx <https://pipxproject.github.io/>`_ (recommended) or ``pip``:\n\n.. code-block:: console\n\n   $ pipx install euporie\n   $ # OR\n   $ python -m pip install --user euporie\n\nYou can also try euporie online `here <https://mybinder.org/v2/gh/joouha/euporie-binder/HEAD?urlpath=%2Feuporie%2F>`_.\n\n********\nFeatures\n********\n\n* Edit and run notebooks in the terminal\n* Run code interactively in a console\n* Display images using terminal graphics (sixel / iterm / kitty)\n* Use Jupyter widgets interactively in the terminal\n* Render rich kernel output (markdown, tables, images, LaTeX, HTML, SVG, & PDF)\n* Tab-completion, line suggestions  and contextual help\n* Convert a console session to a notebook\n* Micro / Vim / Emacs style key-bindings\n\n*****\nUsage\n*****\n\n**Notebooks**\n\n   You can edit a notebook using ``euporie-notebook``, and passing the notebook\'s file path or URI as a command line argument:\n\n   .. code-block:: console\n\n      $ euporie-notebook notebook.ipynb\n\n   Alternatively, launch ``euporie-notebooks`` and open a notebook file by selecting "Open" from the file menu (``Ctrl+O``).\n\n**Console**\n\n   To connect to a Jupyter kernel and run code interactively in a console session, you can run\n\n   .. code-block:: console\n\n      $ euporie-console\n\n   (You can press ``Ctrl+C`` to open the command palette in ``euporie-console``).\n\n**Preview**\n\n   To preview a notebook to the terminal, use the ``euporie-preview`` subcommand:\n\n   .. code-block:: console\n\n      $ euporie-preview notebook.ipynb\n\n**Hub**\n\n   To run euporie hub, a multi-user SSH server for euporie apps, run:\n\n   .. code-block:: console\n\n      $ euporie-hub --port 8022 --host-keys=ssh_host_ed25519_key --client-keys=authorized_keys\n\n   where ``ssh_host_ed25519_key`` is the path to your host key file, and ``authorized_keys`` is a file containing SSH public keys allowed to connect.\n\n*************\nDocumentation\n*************\n\nView the online documentation at: `https://euporie.readthedocs.io/ <https://euporie.readthedocs.io/>`_\n\nThe code is available on GitHub at: `https://github.com/joouha/euporie <https://github.com/joouha/euporie>`_\n\n*************\nCompatibility\n*************\n\nEuporie requires Python 3.8 or later. It works on Linux, Windows and MacOS\n\n\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/euporie.svg\n    :target: https://pypi.python.org/project/euporie/\n    :alt: Latest Version\n\n.. |RTD| image:: https://readthedocs.org/projects/euporie/badge/\n    :target: https://euporie.readthedocs.io/en/latest/\n    :alt: Documentation\n\n.. |PyVer| image:: https://img.shields.io/pypi/pyversions/euporie\n    :target: https://pypi.python.org/project/euporie/\n    :alt: Supported Python versions\n\n.. |Binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/joouha/euporie-binder/HEAD?urlpath=%2Feuporie%2F\n   :alt: Launch with Binder\n\n.. |License| image:: https://img.shields.io/github/license/joouha/euporie.svg\n    :target: https://github.com/joouha/euporie/blob/main/LICENSE\n    :alt: View license\n\n.. |Stars| image:: https://img.shields.io/github/stars/joouha/euporie\n    :target: https://github.com/joouha/euporie/stargazers\n    :alt: ⭐\n',
    'author': 'Josiah Outram Halstead',
    'author_email': 'josiah@halstead.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joouha/euporie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
