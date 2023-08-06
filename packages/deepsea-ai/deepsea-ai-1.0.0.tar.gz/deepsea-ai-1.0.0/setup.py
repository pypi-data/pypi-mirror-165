# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepsea_ai',
 'deepsea_ai.commands',
 'deepsea_ai.database',
 'deepsea_ai.pipeline',
 'deepsea_ai.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.46,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.26.0,<3.0.0',
 'sagemaker>=2.102.0,<3.0.0',
 'tqdm>=4.41.0,<5.0.0']

entry_points = \
{'console_scripts': ['deepsea-ai = deepsea_ai.__main__:cli']}

setup_kwargs = {
    'name': 'deepsea-ai',
    'version': '1.0.0',
    'description': 'DeepSeaAI is a Python package to simplify processing deep sea video in AWS from a command line.',
    'long_description': '[![MBARI](https://www.mbari.org/wp-content/uploads/2014/11/logo-mbari-3b.png)](http://www.mbari.org)\n[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)\n![license-GPL](https://img.shields.io/badge/license-GPL-blue)\n[![Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/downloads/)\n\nDeepSea-AI is a Python package to simplify processing deep sea video in [AWS](https://aws.amazon.com) from a command line. \n\nIt includes reasonable defaults that have been optimized for deep sea video. The goal is to simplify running these algorithms in AWS.\n\nDeepSea-AI currently supports:\n - *Training [YOLOv5](http://github.com/ultralytics/yolov5) object detection models*\n - *Running [YOLOv5](http://github.com/ultralytics/yolov5) detection and tracking pipelines* on video using either:\n   - [DeepSort](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch)\n   - [StrongSort](https://github.com/mikel-brostrom/Yolov5_StrongSORT_OSNet) \n \n\nAuthors: Danelle Cline, [dcline@mbari.org](mailto:dcline@mbari.org), Duane Edgington, [duane@mbari.org](mailto:duane@mbari.org)\n----\n\n### For details on AWS installation, see [docs.mbari.org/deepsea-ai/install](http://docs.mbari.org/deepsea-ai/install)  \n\nAssuming you have completed the AWS installation, install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):\n\n```shell\n$ pip install -U deepsea-ai\n```\n----\n\n\n## Commands\n\n* [`deepsea-ai train --help` - Train a YOLOv5 model and save the model to a bucket](https://docs.mbari.org/deepsea-ai/train/)\n* [`deepsea-ai process --help` - Process one or more videos and save the results to  a bucket](https://docs.mbari.org/deepsea-ai/process/)\n* [`deepsea-ai ecsprocess --help` - Process one or more videos using the Elastic Container Service and save the results to  a bucket](https://docs.mbari.org/deepsea-ai/process/)\n* [`deepsea-ai split --help` - Split your training data; required before the train command.](https://docs.mbari.org/deepsea-ai/split/) \n* `deepsea-ai -h` - Print help message and exit.',
    'author': 'Danelle Cline',
    'author_email': 'dcline@mbari.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mbari-org/deepsea-ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
