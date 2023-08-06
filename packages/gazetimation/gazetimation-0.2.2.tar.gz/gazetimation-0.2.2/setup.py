# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['gazetimation']
install_requires = \
['mediapipe>=0.8.10,<0.9.0',
 'numpy>=1.23.2,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0']

setup_kwargs = {
    'name': 'gazetimation',
    'version': '0.2.2',
    'description': 'Gaze estimation from facial landmarks',
    'long_description': '<div align="center">\n\n<img src="/docs/source/assets/gazetimation_logo.png" />\n\n# Gazetimation\n\n![test](https://github.com/paul-shuvo/gazetimation/actions/workflows/test.yml/badge.svg) [![Docs](https://github.com/paul-shuvo/gazetimation/actions/workflows/docs.yml/badge.svg)](https://paul-shuvo.github.io/gazetimation/) [![PyPI version](https://badge.fury.io/py/gazetimation.svg)](https://badge.fury.io/py/gazetimation) [![License: MIT](https://img.shields.io/github/license/paul-shuvo/gazetimation)](https://opensource.org/licenses/MIT) ![downloads](https://img.shields.io/pypi/dm/gazetimation?color=blue) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/1822d5b3047a4e3596404b4c0e636912)](https://www.codacy.com/gh/paul-shuvo/gazetimation/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=paul-shuvo/gazetimation&amp;utm_campaign=Badge_Grade)\n\n<p>An out of the box solution for gaze estimation.\n\n<img src="https://media4.giphy.com/media/7B7Hhz6w2TCBQikqoL/giphy.gif?cid=790b76112cc0a01f4cc4de64efea7cf5f8c9c0f898ceb1a0&rid=giphy.gif&ct=g" alt="demo" width="600"/>\n\n<!-- ![](docs/source/assets/demo.gif) -->\n\n</div>\n\n## Installation\n\n```console\npip install gazetimation\n```\n\n## Usage\n\n```python\nfrom gazetimation import Gazetimation\ngz = Gazetimation(device=0) # or any other device id\ngz.run()\n```\n\nTo run a video file\n```python\ngz.run(video_path=\'path/to/video\')\n```\n\nTo save as a video file\n```python\ngz.run(video_output_path=\'path/to/video.avi\')\n```\n\nThe [`run`](https://paul-shuvo.github.io/gazetimation/gazetimation.html#gazetimation.Gazetimation.run) method also accepts a handler function for further processing.\n```python\ngz.run(handler=my_handler)\n```\n__Attention__\n\nThe handler function will be called by passing the frame and the gaze information\n\n```python\nif handler is not None:\n    handler([frame, left_pupil, right_pupil, gaze_left_eye, gaze_right_eye])\n```\n\nFor more info check our [docs](https://paul-shuvo.github.io/gazetimation/)\n\n## Issues\n\nIf any issues are found, they can be reported\n[here](https://github.com/paul-shuvo/gazetimation/issues).\n\n## License\n\nThis project is licensed under the\n[MIT](https://opensource.org/licenses/MIT) license.\n\n### Acknowledgement\n\nThis package was inspired from the amazing [Medium\npost](https://medium.com/mlearning-ai/eye-gaze-estimation-using-a-webcam-in-100-lines-of-code-570d4683fe23)\nby Amit Aflalo\n',
    'author': 'Shuvo Kumar Paul',
    'author_email': 'shuvo.k.paul@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paul-shuvo/gazetimation',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
