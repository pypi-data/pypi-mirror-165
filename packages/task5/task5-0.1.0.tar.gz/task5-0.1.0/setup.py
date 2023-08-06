# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['task5']
setup_kwargs = {
    'name': 'task5',
    'version': '0.1.0',
    'description': 'task 5',
    'long_description': '# task_5\n\n# Requirements\n\n  * Python 3.7\n\n> This code makes use of the `f"..."` or [f-string\n> syntax](https://www.python.org/dev/peps/pep-0498/). This syntax was\n> introduced in Python 3.6.\n\n\n# Sample Execution & Output\n\nIf run without command line arguments, using\n\n```\n./precisionEstimate\n```\n\nthe following usage message will be displayed.\n\n```\nUsage: ./estimatePrecision.py num_execs [arbitrary precision]\n```\n\nIf run using\n\n```\n./precisionEstimate 1000000\n```\n\noutput *simliar* to\n\n```\n           float|  3.7247|2.220446049250313e-16\n float-type-hint|  3.6731|2.220446049250313e-16\n      Decimal-28| 31.8602|0.999999999999999999999999999\n```\n\nwill be generated. Note that the `float` and `float-type-hint` lines may vary.\n\n---\n\nAn optional precision command line argument can be supplied to change the\narbitrary precision used by the Python `decimal` module. For example:\n\n```\n./precisionEstimate 1000000 16\n```\n\nwill generate output similar to\n\n```\n           float| 0.3979|2.220446049250313e-16\n float-type-hint| 0.4053|2.220446049250313e-16\n      Decimal-16| 3.1643|0.999999999999999\n```\n',
    'author': 'Dmitry',
    'author_email': 'kocherzhenko.work@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
