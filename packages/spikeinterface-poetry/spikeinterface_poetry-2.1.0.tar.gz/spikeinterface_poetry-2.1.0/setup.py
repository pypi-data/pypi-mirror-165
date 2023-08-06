# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spikeinterface_poetry']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'neo>=0.10.2,<0.11.0',
 'numpy>=1.21,<2.0',
 'packaging>=21.3,<22.0',
 'probeinterface>=0.2.9',
 'spikeinterface',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'all_sorters': ['PyQt5>=5.15.6,<6.0.0',
                 'tridesclous>=1.6.5,<2.0.0',
                 'loky>=3.0.0,<4.0.0',
                 'spyking-circus>=1.1.0,<2.0.0',
                 'herdingspikes>=0.3.99,<0.4.0',
                 'mountainsort4>=1.0.0,<2.0.0',
                 'Cython',
                 'klusta>=3.0.16,<4.0.0',
                 'klustakwik2>=0.2.7,<0.3.0'],
 'docker': ['docker>=5.0.3,<6.0.0'],
 'extractors': ['MEArec>=1.7.2,<2.0.0', 'pynwb>=2.0.0,<3.0.0'],
 'extractors:python_version >= "3.8" and python_version < "3.9"': ['sonpy>=1.8.1,<2.0.0'],
 'extractors:python_version >= "3.9" and python_version < "3.10"': ['sonpy>=1.9.1,<2.0.0'],
 'full': ['zarr>=2.12.0,<3.0.0',
          'h5py>=3.6.0,<4.0.0',
          'matplotlib>=3.5.1,<4.0.0'],
 'full:python_version >= "3.7" and python_version < "3.8"': ['pandas',
                                                             'scipy>=1.7.0,<2.0.0'],
 'full:python_version >= "3.8"': ['networkx>=2.7,<3.0', 'pandas>=1.4.1,<2.0.0'],
 'full:python_version >= "3.8" and python_version < "3.11"': ['scipy>=1.8.0,<2.0.0'],
 'herdingspikes': ['herdingspikes>=0.3.99,<0.4.0'],
 'jupyter': ['jupyter>=1.0.0,<2.0.0'],
 'klusta': ['Cython', 'klusta>=3.0.16,<4.0.0', 'klustakwik2>=0.2.7,<0.3.0'],
 'mountainsort': ['mountainsort4>=1.0.0,<2.0.0'],
 'phy': ['phy>=2.0b5,<3.0'],
 'spyking-circus': ['PyQt5>=5.15.6,<6.0.0', 'spyking-circus>=1.1.0,<2.0.0'],
 'spython': ['spython>=0.1.18,<0.2.0'],
 'test': ['zarr>=2.12.0,<3.0.0',
          'MEArec>=1.7.2,<2.0.0',
          'pynwb>=2.0.0,<3.0.0',
          'PyQt5>=5.15.6,<6.0.0',
          'tridesclous>=1.6.5,<2.0.0',
          'loky>=3.0.0,<4.0.0',
          'spyking-circus>=1.1.0,<2.0.0',
          'herdingspikes>=0.3.99,<0.4.0',
          'pyEDFlib>=0.1.30,<0.2.0',
          'pymde>=0.1.15,<0.2.0',
          'torch>=1.12.1,<2.0.0',
          'pynndescent>=0.5.7,<0.6.0'],
 'test:python_version >= "3.8" and python_version < "3.9"': ['sonpy>=1.8.1,<2.0.0'],
 'test:python_version >= "3.9" and python_version < "3.10"': ['sonpy>=1.9.1,<2.0.0'],
 'tridesclous': ['PyQt5>=5.15.6,<6.0.0',
                 'tridesclous>=1.6.5,<2.0.0',
                 'pyopencl>=2022.1,<2023.0',
                 'loky>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'spikeinterface-poetry',
    'version': '2.1.0',
    'description': 'Poetry packaging with extras for working with spikeinterface',
    'long_description': "# The poetry of Spikeinterface\n\nThis package integrates [spikeinterface](https://spikeinterface.readthedocs.io/en/latest/) into poetry packaging to ensure stability.\n\nMy personal experience is that installing `spikeinterface` is smoother this way.\n\n## Installation\n\nRun the following in shell:\n```shell\npip install spikeinterface-poetry\n```\n\nYou can install spikesorters such as `tridesclous`, `spyking-circus`, `herdingspikes`, `klusta`, `mountainsort` easily:\n```shell\npip install spikeinterface-poetry[<spike sorter name>]\n```\nYou can also install `phy`, `docker`, and `spython` (singularity) the same way as above.\n\n## Important remarks\n\nThis package is maintained solely by me, and not the original authors of `spikeinterface`. Please don't make any issues related to the packaging in the `spikeinterface` repository. Should you have any problems running any of the spikesorters, contact the author of that spike sorter.\n\nI also can't and don't guarantee that every component of spikeinterface to work as intended by the original authors. This is the nature of downstream packaging by a 3rd party. This should be less of an issue once poetry has been added to `spikeinterface`.\n",
    'author': 'Can H. Tartanoglu',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/caniko/spikeinterface_poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
