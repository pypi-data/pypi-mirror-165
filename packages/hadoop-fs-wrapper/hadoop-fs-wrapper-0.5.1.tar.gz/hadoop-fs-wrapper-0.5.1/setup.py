# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hadoop_fs_wrapper', 'hadoop_fs_wrapper.models', 'hadoop_fs_wrapper.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['pyspark>=3.3,<3.4']

setup_kwargs = {
    'name': 'hadoop-fs-wrapper',
    'version': '0.5.1',
    'description': 'Python Wrapper for Hadoop Java API',
    'long_description': '# Hadoop FileSystem Java Class Wrapper \nTyped Python wrappers for [Hadoop FileSystem](https://hadoop.apache.org/docs/stable/api/org/apache/hadoop/fs/FileSystem.html) class family.\n\n## Installation\nYou can install this package from `pypi` on any Hadoop or Spark runtime:\n```commandline\npip install hadoop-fs-wrapper\n```\n\nSelect a version that matches hadoop version you are using:\n\n| Hadoop Version | Compatible hadoop-fs-wrapper version |\n|----------------|:------------------------------------:|\n| 3.2.x          |                0.4.x                 |\n| 3.3.x          |             0.4.x, 0.5.x             |\n\n## Usage\nCommon use case is accessing Hadoop FileSystem from Spark session object:\n\n```python\nfrom hadoop_fs_wrapper.wrappers.file_system import FileSystem\n\nfile_system = FileSystem.from_spark_session(spark=spark_session)\n```\n\nThen, for example, one can check if there are any files under specified path:\n```python\nfrom hadoop_fs_wrapper.wrappers.file_system import FileSystem\n\ndef is_valid_source_path(file_system: FileSystem, path: str) -> bool:\n    """\n     Checks whether a regexp path refers to a valid set of paths\n    :param file_system: pyHadooopWrapper FileSystem\n    :param path: path e.g. (s3a|abfss|file|...)://hello@world.com/path/part*.csv\n    :return: true if path resolves to existing paths, otherwise false\n    """\n    return len(file_system.glob_status(path)) > 0\n```\n\n## Contribution\n\nCurrently basic filesystem operations (listing, deleting, search, iterative listing etc.) are supported. If an operation you require is not yet wrapped,\nplease open an issue or create a PR.\n\nAll changes are tested against Spark 3.2/3.3 running in local mode.',
    'author': 'ECCO Sneaks & Data',
    'author_email': 'esdsupport@ecco.com',
    'maintainer': 'GZU',
    'maintainer_email': 'gzu@ecco.com',
    'url': 'https://github.com/SneaksAndData/hadoop-fs-wrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
