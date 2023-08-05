# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmem_plugin_kafka', 'cmem_plugin_kafka.workflow']

package_data = \
{'': ['*']}

install_requires = \
['cmem-plugin-base>=2.1.0,<3.0.0',
 'confluent-kafka==1.8.2',
 'defusedxml>=0.7.1,<0.8.0']

extras_require = \
{':sys_platform == "darwin"': ['confluent-kafka @ '
                               'https://files.pythonhosted.org/packages/fb/16/d04dded73439266a3dbcd585f1128483dcf509e039bacd93642ac5de97d4/confluent-kafka-1.8.2.tar.gz']}

setup_kwargs = {
    'name': 'cmem-plugin-kafka',
    'version': '1.0.0',
    'description': 'Send messages from Apache Kafka',
    'long_description': '# cmem-plugin-kafka\n\nThis eccenca Corporate Memory plugin allows for sending messages to Apache Kafka.\n\n',
    'author': 'eccenca',
    'author_email': 'cmempy-developer@eccenca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eccenca/cmem-plugin-kafka',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
