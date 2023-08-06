# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dazed']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0']

extras_require = \
{'pandas': ['pandas>=1.1.5,<2.0.0']}

setup_kwargs = {
    'name': 'dazed',
    'version': '1.0.3',
    'description': 'A confusion matrix package.',
    'long_description': '.. |linting| image:: https://github.com/calmdown13/dazed/workflows/Linting/badge.svg\n.. |tests| image:: https://github.com/calmdown13/dazed/workflows/Tests/badge.svg\n.. |pypi| image:: https://img.shields.io/pypi/v/dazed.svg\n   :target: https://pypi.org/project/dazed/\n.. |rtd| image:: https://readthedocs.org/projects/dazed/badge/\n   :target: https://dazed.readthedocs.io/\n\n|linting| |tests| |pypi| |rtd|\n\n*************************************\n💫 Dazed - A Confusion Matrix Package\n*************************************\n\nDazed is a little confusion matrix package designed to make your life easier.\nIts key features are:\n\n-  support for lots of different data formats (sparse integers, sparse strings, one-hot arrays, dataframes)\n-  support for multilabel data\n-  ability to list most confused labels\n-  ability to index sample information by confused label names\n-  prints out nicely\n\n\n************\nInstallation\n************\nFor the basic installation:\n\n.. code-block:: console\n\n   $ pip install dazed\n\nTo include pandas dataframe support:\n\n.. code-block:: console\n\n   $ pip install dazed[pandas]\n\n\n***********\nBasic Usage\n***********\nTo give you an idea of why you might want to use dazed, here is a toy example\ndemonstrating the kind of investigation it was designed to help with. Note: I\nam using sparse string labels here but dazed\'s interfaces can cope with integers,\nonehot encoded arrays and dataframes as well (refer to the\n`API Reference <https://dazed.readthedocs.io/en/latest/api_reference.html>`_\nfor more information).\n\nImagine your building a machine learning model to catalogue a pet store\'s\ninventory (primarily cats, dogs and fish). The owner has given you an image of\neach animal and you\'ve trained your model and made some predictions. Your data\nlooks like:\n\n.. code-block::\n\n   filenames = [\n      "img0.jpg", "img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg", "img5.jpg"\n   ]\n   truth = ["cat", "dog", "cat", "dog", "fish", "dog"]\n   pred = ["cat", "dog", "dog", "cat", "fish", "cat"]\n\nIn order to understand how your model is doing, you make a quick confusion\nmatrix:\n\n.. code-block::\n\n   from dazed import ConfusionMatrix\n\n   cm = ConfusionMatrix.from_sparse(truth, pred, info=filenames)\n   print(cm)\n\n.. code-block:: console\n\n     | 0 1 2     index | label\n   ---------     -------------\n   0 | 1 1 0         0 |   cat\n   1 | 2 1 0         1 |   dog\n   2 | 0 0 1         2 |  fish\n   ---------     -------------\n\nFrom the confusion matrix it looks like the model might be prone to thinking that\ndogs are actually cats. To double check:\n\n.. code-block::\n\n   cm.most_confused()\n\n.. code-block:: console\n\n   [(\'dog\', \'cat\', 2), (\'cat\', \'dog\', 1)]\n\nAh yes, dogs were predicted to be cats twice and cats to be dogs\nonce. To try and find out what the problem might be you decide that you should\ncheck the images. To get the appropiate images:\n\n.. code-block::\n\n   cm.label_pair_info("dog", "cat")\n\n.. code-block:: console\n\n   [\'img3.jpg\', \'img5.jpg\']\n\nUpon investigating the images you notice that both dogs are white. You\ndecide to go back through and label your images for animal colour.\n\n.. code-block::\n\n   truth = [\n      ["cat", "white"],\n      ["dog", "brown"],\n      ["cat", "brown"],\n      ["dog", "white"],\n      ["fish", "orange"],\n      ["dog", "white"]\n   ]\n   pred = [\n      ["cat", "white"],\n      ["dog", "brown"],\n      ["dog", "brown"],\n      ["cat", "white"],\n      ["fish", "orange"],\n      ["cat", "white"]\n   ]\n   cm = ConfusionMatrix.from_sparse(\n      truth, pred, info=filenames, multilabel=True\n   )\n   print(cm)\n\n.. code-block:: console\n\n     | 0 1 2 3 4     index |        label\n   -------------     --------------------\n   0 | 0 0 1 0 0         0 |   cat, brown\n   1 | 0 1 0 0 0         1 |   cat, white\n   2 | 0 0 1 0 0         2 |   dog, brown\n   3 | 0 2 0 0 0         3 |   dog, white\n   4 | 0 0 0 0 1         4 | fish, orange\n   -------------     --------------------\n\nHmm looks like all white dogs were miss classified as white cats.\n\n.. code-block::\n\n   cm.most_confused()\n\n.. code-block:: console\n\n   [(\'dog, white\', \'cat, white\', 2), (\'cat, brown\', \'dog, brown\', 1)]\n\nAh yes looks like your model might be basing much of its prediction on animal\ncolour, maybe time to go collect some more data.\n\nTo find out more about dazed take a look at the `API Reference <https://dazed.readthedocs.io/en/latest/api_reference.html>`_.\n',
    'author': 'calmdown13',
    'author_email': 'callum@callumdownie.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
