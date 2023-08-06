# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mextractor']

package_data = \
{'': ['*']}

install_requires = \
['pydantic-yaml>=0.8.0,<0.9.0',
 'pydantic>=1.9.2,<2.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'webp>=0.1.4,<0.2.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['numpy>=1.21.0,<2.0.0'],
 ':python_version >= "3.8" and python_version < "3.11"': ['numpy'],
 'extract': ['opencv-python>=4.6.0,<5.0.0', 'ffmpeg-python>=0.2.0,<0.3.0']}

setup_kwargs = {
    'name': 'mextractor',
    'version': '1.2.1',
    'description': 'mextractor can extract media metadata to YAML and read them',
    'long_description': '# mextractor: media metadata extractor\n\nVideos and images can be large. \n\n## Installation\n\nDownload and install from PyPi with `pip`:\n\n```shell\npip install mextractor\n```\n\n## Usage\n\n### Extract and dump metadata\n```python\nimport mextractor\n\nmetadata = mextractor.extract_and_dump(path_to_dump, path_to_media)\n```\n\n### Load media\n\n#### Video\n\n```python\nimport mextractor\n\nvideo_metadata = mextractor.parse_file(path_to_metadata)\n\nprint(video_metadata.fps)\nprint(video_metadata.frames)\nprint(video_metadata.resolution)\nprint(video_metadata.seconds)\nprint(video_metadata.path)\nprint(video_metadata.bytes)\n```\n\n#### Image\n\n```python\nimport mextractor\n\nimage_metadata = mextractor.parse_file(path_to_metadata)\n\nprint(image_metadata.resolution)\nprint(image_metadata.path)\nprint(image_metadata.bytes)\n```\n',
    'author': 'Can H. Tartanoglu',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/mextractor/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
