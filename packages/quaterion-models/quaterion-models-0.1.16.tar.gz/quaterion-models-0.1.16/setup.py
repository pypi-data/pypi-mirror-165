# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quaterion_models',
 'quaterion_models.encoders',
 'quaterion_models.encoders.extras',
 'quaterion_models.heads',
 'quaterion_models.modules',
 'quaterion_models.types',
 'quaterion_models.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22,<2.0', 'torch>=1.8.2']

extras_require = \
{'fasttext': ['gensim>=4.1.2,<5.0.0']}

setup_kwargs = {
    'name': 'quaterion-models',
    'version': '0.1.16',
    'description': 'The collection of building blocks to build fine-tunable similarity learning models',
    'long_description': '# Quaterion Models\n\n`quaterion-models` is a part of [`Quaterion`](https://github.com/qdrant/quaterion), similarity learning framework.\nIt is kept as a separate package to make servable models lightweight and free from training dependencies.\n\nIt contains definition of base classes, used for model inference, as well as the collection of building blocks for building fine-tunable similarity learning models.\nThe documentation can be found [here](https://quaterion-models.qdrant.tech/).\n\nIf you are looking for the training-related part of Quaterion, please see the [main repository](https://github.com/qdrant/quaterion) instead.\n\n## Install\n\n```bash\npip install quaterion-models\n```\n\nIt makes sense to install `quaterion-models` independent of the main framework if you already have trained model\nand only need to make inference.\n\n## Load and inference\n\n```python\nfrom quaterion_models import SimilarityModel\n\nmodel = SimilarityModel.load("./path/to/saved/model")\n\nembeddings = model.encode([\n    {"description": "this is an example input"},\n    {"description": "you may have a different format"},\n    {"description": "the output will be a numpy array"},\n    {"description": "of size [batch_size, embedding_size]"},\n])\n```\n\n## Content\n\n* `SimilarityModel` - main class which contains encoder models with the head layer\n* Base class for Encoders\n* Base class and various implementations of the Head Layers\n* Additional helper functions\n',
    'author': 'Quaterion Authors',
    'author_email': 'team@qdrant.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qdrant/quaterion-models',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
