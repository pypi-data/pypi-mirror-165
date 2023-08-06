# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trustee', 'trustee.enums', 'trustee.report', 'trustee.utils']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.8.1',
 'matplotlib>=3.3.1,<4.0.0',
 'numpy>=1.19.0',
 'pandas>=1.1.0,<2.0.0',
 'prettytable==3.0.0',
 'rootpath>=0.1.1,<0.2.0',
 'scikit-learn>=0.23.2',
 'scipy>=1.4.1,<2.0.0',
 'setuptools>=57.0.0,<58.0.0',
 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'trustee',
    'version': '1.1.1',
    'description': 'This package implements the Trustee framework to extract decision tree explanation from black-box ML models.',
    'long_description': '<img src="https://github.com/TrusteeML/trustee/blob/master/docs/_static/logo.png?raw=true" alt="Trustee" width="400"/>\n\nThis package implements the `trustee` framework to extract decision tree explanation from black-box ML models.\nFor more information, please visit the [documentation website](https://trusteeml.github.io).\n\nStandard AI/ML development pipeline extended by Trustee.\n<img alt="Trustee" src="https://github.com/TrusteeML/trustee/blob/master/docs/_static/flowchart.png?raw=true"  width="800">\n\nGetting Started\n---------------\n\nThis section contains basic information and instructions to get started with Trustee.\n\n### Python Version\n\nTrustee supports `Python >=3.7`.\n\n### Install Trustee\n\nUse the following command to install Trustee:\n\n```\n$ pip install trustee\n```\n\n### Sample Code\n\n```\nfrom sklearn import datasets\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import classification_report\n\nfrom trustee import ClassificationTrustee\n\nX, y = datasets.load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)\n\nclf = RandomForestClassifier(n_estimators=100)\nclf.fit(X_train, y_train)\ny_pred = clf.predict(X_test)\n\ntrustee = ClassificationTrustee(expert=clf)\ntrustee.fit(X_train, y_train, num_iter=50, num_stability_iter=10, samples_size=0.3, verbose=True)\ndt = trustee.explain()\ndt_y_pred = dt.predict(X_test)\n\nprint("Model explanation global fidelity report:")\nprint(classification_report(y_pred, dt_y_pred))\nprint("Model explanation score report:")\nprint(classification_report(y_test, dt_y_pred))\n```\n\n### Usage Examples\n\nFor simple usage examples of Trustee and TrustReport, please check the `examples/` directory.\n\n### Other Use Cases\n\nFor other examples and use cases of how Trustee can used to scrutinize ML models, listed in the table below, please check our [Use Cases repository](https://github.com/TrusteeML/emperor).\n\n | Use Case           | Description                                                                                                                                                 |\n | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |\n | heartbleed\\_case/  | Trustee application to a Random Forest Classifier for an Intrustion Detection System, trained with CIC-IDS-2017 dataset pre-computed features.              |\n | kitsune\\_case/     | Trustee application to Kitsune model for anomaly detection in network traffic, trained with features extracted from Kitsune\\\'s Mirai attack trace.          |\n | iot\\_case/         | Trustee application to Random Forest Classifier to distguish IoT devices, trained with features extracted from the pcaps from the UNSW IoT Dataset.         |\n | moon\\_star\\_case/  | Trustee application to Neural Network Moon and Stars Shortcut learning toy example.                                                                         |\n | nprint\\_ids\\_case/ | Trustee application to the nPrintML AutoGluon Tabular Predictor for an Intrustion Detection System, also trained using pcaps from the CIC-IDS-2017 dataset. |\n | nprint\\_os\\_case/  | Trustee application to the nPrintML AutoGluon Tabular Predictor for OS Fingerprinting, also trained using with pcaps from the CIC-IDS-2017 dataset.         |\n | pensieve\\_case/    | Trustee application to the Pensieve RL model for adaptive bit-rate prediction, and comparison to related work Metis.                                        |\n | vpn\\_case/         | Trustee application the 1D-CNN trained to detect VPN traffic trained with the ISCX VPN-nonVPN dataset.                                                      |\n\n### Supported AI/ML Libraries\n\n | Library      | Supported          |\n | ------------ | ------------------ |\n | scikit-learn | :white_check_mark: |\n | Keras        | :white_check_mark: |\n | Tensorflow   | :white_check_mark: |\n | PyTorch      | :white_check_mark: |\n | AutoGluon    | :white_check_mark: |\n\n## Citing us\n\n```\n@inproceedings{Jacobs2022,\n\ttitle        = {AI/ML and Network Security: The Emperor has no Clothes},\n\tauthor       = {A. S. Jacobs and R. Beltiukov and W. Willinger and R. A. Ferreira and A. Gupta and L. Z. Granville},\n\tyear         = 2022,\n\tbooktitle    = {Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security},\n\tlocation     = {Los Angeles, CA, USA},\n\tpublisher    = {Association for Computing Machinery},\n\taddress      = {New York, NY, USA},\n\tseries       = {CCS \'22}\n}\n```',
    'author': 'Arthur Selle Jacobs',
    'author_email': 'asjacobs@inf.ufrgs.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://trusteeml.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
