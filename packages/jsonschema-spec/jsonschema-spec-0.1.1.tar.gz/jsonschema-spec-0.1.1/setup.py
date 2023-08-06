# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonschema_spec', 'jsonschema_spec.handlers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1',
 'jsonschema>=4.0.0,<5.0.0',
 'pathable>=0.4.1,<0.5.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'jsonschema-spec',
    'version': '0.1.1',
    'description': 'JSONSchema Spec with object-oriented paths',
    'long_description': '***************\nJSONSchema Spec\n***************\n\n.. image:: https://img.shields.io/pypi/v/jsonschema-spec.svg\n     :target: https://pypi.python.org/pypi/jsonschema-spec\n.. image:: https://travis-ci.org/p1c2u/jsonschema-spec.svg?branch=master\n     :target: https://travis-ci.org/p1c2u/jsonschema-spec\n.. image:: https://img.shields.io/codecov/c/github/p1c2u/jsonschema-spec/master.svg?style=flat\n     :target: https://codecov.io/github/p1c2u/jsonschema-spec?branch=master\n.. image:: https://img.shields.io/pypi/pyversions/jsonschema-spec.svg\n     :target: https://pypi.python.org/pypi/jsonschema-spec\n.. image:: https://img.shields.io/pypi/format/jsonschema-spec.svg\n     :target: https://pypi.python.org/pypi/jsonschema-spec\n.. image:: https://img.shields.io/pypi/status/jsonschema-spec.svg\n     :target: https://pypi.python.org/pypi/jsonschema-spec\n\nAbout\n#####\n\nJSONSchema Spec with object-oriented paths\n\nKey features\n************\n\n* Traverse elements like paths\n* Access spec on demand with separate dereferencing accessor layer\n\nInstallation\n############\n\n::\n\n    $ pip install jsonschema-spec\n\nAlternatively you can download the code and install from the repository:\n\n.. code-block:: bash\n\n   $ pip install -e git+https://github.com/p1c2u/jsonschema-spec.git#egg=jsonschema_spec\n\n\nUsage\n#####\n\n.. code-block:: python\n\n   from jsonschema_spec import Spec\n   \n   d = {\n       "openapi": "3.0.1",\n       "info": {\n            "$ref": "#/components/Version",\n       },\n       "paths": {},\n       "components": {\n           "Version": {\n               "title": "Minimal",\n               "version": "1.0",\n            },\n       },\n   }\n   \n   spec = Spec.from_dict(d)\n   \n   # Concatenate paths with /\n   info = spec / "info"\n   \n   # Stat path keys\n   "title" in info\n   \n   # Open path dict\n   with info.open() as info_dict:\n       print(info_dict)\n\n\nRelated projects\n################\n\n* `openapi-core <https://github.com/p1c2u/openapi-core>`__\n   Python library that adds client-side and server-side support for the OpenAPI.\n* `openapi-spec-validator <https://github.com/p1c2u/openapi-spec-validator>`__\n   Python library that validates OpenAPI Specs against the OpenAPI 2.0 (aka Swagger) and OpenAPI 3.0 specification\n* `openapi-schema-validator <https://github.com/p1c2u/openapi-schema-validator>`__\n   Python library that validates schema against the OpenAPI Schema Specification v3.0.\n\nLicense\n#######\n\nCopyright (c) 2017-2022, Artur Maciag, All rights reserved. Apache v2\n',
    'author': 'Artur Maciag',
    'author_email': 'maciag.artur@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/p1c2u/jsonschema-spec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
