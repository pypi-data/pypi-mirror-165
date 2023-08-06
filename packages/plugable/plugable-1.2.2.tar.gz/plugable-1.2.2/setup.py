# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['plugable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'plugable',
    'version': '1.2.2',
    'description': 'A framework for writing extensible Python components',
    'long_description': '# Plugable: A Python Plugin Framework\n\n## Badges:\n - **Build:** [![Build Status](https://travis-ci.com/jacobneiltaylor/plugable.svg?branch=master)](https://travis-ci.com/jacobneiltaylor/plugable)\n - **Coverage:** [![Coverage Status](https://coveralls.io/repos/github/jacobneiltaylor/plugable/badge.svg?branch=master)](https://coveralls.io/github/jacobneiltaylor/plugable?branch=master)\n\n\nThis package exposes a framework for writing extensible applications.\n\nSpecifically, it allows consumers to mark an abstract class as "Plugable", using standard inheritance semantics and ABC decorators:\n\n```python3\nfrom abc import abstractmethod\nfrom plugable import Plugable\n\nclass AbstractInterface(Plugable):\n    @abstractmethod\n    def example(self):\n        pass\n```\n\nFollowing this, you can create subclasses for differing implementations, and register them with the `AbstractInterface` registry, like so:\n\n```python3\nclass ExampleOne(AbstractInterface, register="one"): # Integrated registration\n    def example(self):\n        print("You ran ExampleOne!")\n\nclass ExampleTwo(AbstractInterface):\n    def example(self):\n        print("You ran ExampleTwo!")\n\nAbstractInterface.registry.register("two", ExampleTwo) # Explicit registration\n```\n\nFinally, you can access and consume the registered implementations, like so:\n\n```python3\nAbstractInterface.get("one").example()  # You ran ExampleOne!\nAbstractInterface.get("two").example()  # You ran ExampleTwo!\n```\n\n',
    'author': 'Jacob Neil Taylor',
    'author_email': 'me@jacobtaylor.id.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
