# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eurlex']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'fire>=0.4.0,<0.5.0',
 'halo>=0.0.31,<0.0.32',
 'importlib-metadata==1.4',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.3.0,<2.0.0',
 'pdfminer.six>=20220524,<20220525',
 'requests>=2.28.1,<3.0.0',
 'sparql-dataframe>=0.4,<0.5']

setup_kwargs = {
    'name': 'pyeurlex',
    'version': '0.1.5',
    'description': 'This is a python module to create SPARQL queries for the EU Cellar repository, run them and subsequently download their data. Notably, it directly supports all resource types.',
    'long_description': '# pyeurlex package\n\nThis is a python module to create SPARQL queries for the EU Cellar repository, run them and subsequently download their data. Notably, it directly supports all resource types. \n\n## Usage\n\nImport and instantiate the moduel\n\n```\nfrom eurlex import Eurlex\neur = Eurlex()\n```\n\nThen you can construct you query. (or alternatively you can use your own or one constructed via the wizard https://op.europa.eu/en/advanced-sparql-query-editor\n\n```\nq = eur.make_query(resource_type = "caselaw", order = True, limit = 10)\nprint(q)\n```\n\nFinally, you can run this query.\n\n```\nd = eur.query_eurlex(q)  # where q is a query generated in a previous step or a string defined by you\nprint(d)\n```\nThis will return a pandas data frame of the results. Its columns depend on the the fields that you included. At the moment, not all fields are named properly in the dataframe and you will have to set their name manually if desired.\n\nOnce you pick a single url or identifier from the df, you can download a notice or data based on that indentifier. To download the notices as xml, use `download_xml()` as below.\n\n```\nx = eur.download_xml("32014R0001", notice="tree") # without the file parameter to specify the filename, the celex number will be used.\nprint(x)\n```\n\nTo get data associated with an identifier, use `get_data()`. This will return the data as a string,\n```\nd = eur.get_data("http://publications.europa.eu/resource/celex/32016R0679", type="text")\nprint(d)\n```\n\n# Why another package/module?\n\nInspired by the  R based eurlex package, which helped a lot with the SPARQL construction and understanding and general inspiration.\nThere is also https://github.com/seljaseppala/eu_corpus_compiler but that also only does regulatory/legislative documents. There is https://pypi.org/project/eurlex/, but it for example does not have a way to generate SPARQL queries and is also very focused on legislation. In addition, while internally it uses SPARQL and cellar as well, its documentation is focused on accessing and processing documents via CELEX number, which is not really helpful to me. Thus, this package was born.\n',
    'author': 'step21',
    'author_email': 'step21@devtal.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
