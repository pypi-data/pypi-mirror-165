# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guipy', 'guipy.components']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'guipylib',
    'version': '0.2.0',
    'description': 'UI library for pygame',
    'long_description': '# Guipy\n![Python](https://img.shields.io/badge/python-3-blue.svg?v=1)\n![Version](https://img.shields.io/pypi/v/guipylib.svg?v=1)\n![License](https://img.shields.io/pypi/l/guipylib.svg?v=1)\n\nPygame UI Library built by Casey (@caseyhackerman) and Jason\n\n## Installation\n```\npip install guipylib\n```\nor with poetry\n```\npoetry add guipylib\n```\n\n## Example\n<p align="center">\n<img alt="Slider" src="./docs/imgs/slider.gif" width="600" />\n</p>\n\n\n```python\nimport sys\nimport colorsys\n\nfrom guipy.manager import GUIManager\nfrom guipy.components.slider import Slider\n\nimport pygame \n\npygame.init()\n\nwinW = 1280\nwinH = 720\n\nroot = pygame.display.set_mode((winW, winH))\n\nman = GUIManager()\n\nmySlider = Slider(height=50, width=500, thickness=5,\n                    radius=12, initial_val=.4)\nmySlider2 = Slider(height=50, width=500, thickness=5,\n                    radius=12, initial_val=0)\nmySlider3 = Slider(height=50, width=500, thickness=5,\n                    radius=12, initial_val=.5)\nmySlider4 = Slider(height=50, width=500, thickness=5,\n                    radius=12, initial_val=.5)\n\nman.add(mySlider, (0, 25))\nman.add(mySlider2, (0, 75))\nman.add(mySlider3, (0, 125))\nman.add(mySlider4, (0, 175))\n\nwhile True:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            sys.exit()\n\n    root.fill((50, 50, 50))\n\n    color = tuple(i * 255 for i in colorsys.hls_to_rgb(mySlider2.get_val(),\n                    mySlider3.get_val(), mySlider4.get_val()))\n\n    pygame.draw.circle(root, color, (winW/2, winH/2),\n                        10 + mySlider.get_val() * 100)\n\n    man.draw(root)\n    man.update(pygame.mouse.get_pos())\n    pygame.display.update()\n\n```\n\n## Documentation\nCheck out some helpful guides and API references [here](https://zjjc123.github.io/guipy/)',
    'author': 'Casey Culbertson, Jason Zhang',
    'author_email': 'me@jasonzhang.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Zjjc123/guipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
