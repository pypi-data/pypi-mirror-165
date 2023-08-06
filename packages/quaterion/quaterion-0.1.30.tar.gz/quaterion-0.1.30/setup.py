# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quaterion',
 'quaterion.dataset',
 'quaterion.distances',
 'quaterion.eval',
 'quaterion.eval.accumulators',
 'quaterion.eval.group',
 'quaterion.eval.pair',
 'quaterion.eval.samplers',
 'quaterion.loss',
 'quaterion.loss.extras',
 'quaterion.train',
 'quaterion.train.cache',
 'quaterion.train.callbacks',
 'quaterion.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'mmh3>=3.0.0,<4.0.0',
 'protobuf>=3.9.2,<3.20',
 'pytorch-lightning>=1.6.4,<2.0.0',
 'quaterion-models>=0.1.16,<0.2.0',
 'rich>=12.4.4,<13.0.0',
 'torch>=1.8.2',
 'torchmetrics<=0.8.2']

extras_require = \
{'full': ['pytorch-metric-learning>=1.3.0,<2.0.0'],
 'pytorch-metric-learning': ['pytorch-metric-learning>=1.3.0,<2.0.0']}

setup_kwargs = {
    'name': 'quaterion',
    'version': '0.1.30',
    'description': 'Similarity Learning fine-tuning framework',
    'long_description': '<p align="center">\n  <img height="100" src="docs/imgs/logo.svg" alt="Quaterion">\n</p>\n\n<p align="center">\n    <b>Blazing fast framework for fine-tuning Similarity Learning models</b>\n</p>\n\n<p align=center>\n    <a href="https://pypi.org/project/quaterion"><img src="https://img.shields.io/pypi/v/quaterion?label=pypi" alt="Version" /></a>\n    <a href="https://github.com/qdrant/quaterion/actions/workflows/test.yml"><img src="https://github.com/qdrant/quaterion/actions/workflows/test.yml/badge.svg" alt="Tests status"></a>\n    <a href="https://qdrant.to/discord"><img src="https://img.shields.io/badge/Discord-Qdrant-5865F2.svg?logo=discord" alt="Discord"></a>\n    <a href="https://quaterion.qdrant.tech"><img src="https://img.shields.io/badge/Learn-Docs%20%26%20Tutorials-success" alt="Docs & Tutorials" /></a>\n</p>\n\n>  A dwarf on a giant\'s shoulders sees farther of the two\n\nQuaterion is a framework for fine-tuning similarity learning models.\nThe framework closes the "last mile" problem in training models for semantic search, recommendations, anomaly detection, extreme classification, matching engines, e.t.c.\n\nIt is designed to combine the performance of pre-trained models with specialization for the custom task while avoiding slow and costly training.\n\n\n## Features\n\n* 🌀 **Warp-speed fast**: With the built-in caching mechanism, Quaterion enables you to train thousands of epochs with huge batch sizes even on *laptop GPU*.\n\n<p align="center">\n  <img alt="Regular vs Cached Fine-Tuning" src="https://storage.googleapis.com/quaterion/docs/new-cmp-demo.gif">\n</p>\n\n* 🐈\u200d **Small data compatible**: Pre-trained models with specially designed head layers allow you to benefit even from a dataset you can label *in one day*.\n\n\n* 🏗️ **Customizable**: Quaterion allows you to re-define any part of the framework, making it flexible even for large-scale and sophisticated training pipelines.\n\n\n* 🌌 **Scalable**: Quaterion is built on top of [PyTorch Lightning](https://github.com/Lightning-AI/lightning) and inherits all its scalability, cost-efficiency, and reliability perks.\n\n## Installation\n\nTL;DR:\n\nFor training:\n```bash\npip install quaterion\n```\n\nFor inference service:\n```bash\npip install quaterion-models\n```\n\n---\n\nQuaterion framework consists of two packages - `quaterion` and [`quaterion-models`](https://github.com/qdrant/quaterion-models).\n\nSince it is not always possible or convenient to represent a model in ONNX format (also, it **is supported**), the Quaterion keeps a very minimal collection of model classes, which might be required for model inference, in a [separate package](https://github.com/qdrant/quaterion-models).\n\nIt allows avoiding installing heavy training dependencies into inference infrastructure: `pip install quaterion-models`\n\nAt the same time, once you need to have a full arsenal of tools for training and debugging models, it is available in one package: `pip install quaterion`\n\n\n## Docs 📓\n\n* [Quick Start](https://quaterion.qdrant.tech/getting_started/quick_start.html) Guide\n* Minimal working [examples](./examples)\n\nFor a more in-depth dive, check out our end-to-end tutorials:\n\n- Fine-tuning NLP models - [Q&A systems](https://quaterion.qdrant.tech/tutorials/nlp_tutorial.html)\n- Fine-tuning CV models - [Similar Cars Search](https://quaterion.qdrant.tech/tutorials/cars-tutorial.html)\n\nTutorials for advanced features of the framework:\n\n- [Cache tutorial](https://quaterion.qdrant.tech/tutorials/cache_tutorial.html) - How to make training fast.\n- [Head Layers: Skip Connection](https://quaterion.qdrant.tech/tutorials/head_layers_skip_connection.html) - How to avoid forgetting while fine-tuning\n- [Embedding Confidence](https://quaterion.qdrant.tech/tutorials/embedding_confidence.html) - how do I know that the model is sure about the output vector?\n- [Vector Collapse Prevention](https://quaterion.qdrant.tech/tutorials/triplet_loss_trick.html) - how to prevent vector space collapse in Triplet Loss\n\n\n## Community\n\n* Join our [Discord channel](https://qdrant.to/discord)\n* Follow us on [Twitter](https://qdrant.to/twitter)\n* Subscribe to our [Newsletters](https://qdrant.to/newsletter)\n* Write us an email [info@qdrant.tech](mailto:info@qdrant.tech)\n\n## License\n\nQuaterion is licensed under the Apache License, Version 2.0. View a copy of the [License file](https://github.com/qdrant/quaterion/blob/master/LICENSE).\n',
    'author': 'Quaterion Authors',
    'author_email': 'team@quaterion.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qdrant/quaterion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
