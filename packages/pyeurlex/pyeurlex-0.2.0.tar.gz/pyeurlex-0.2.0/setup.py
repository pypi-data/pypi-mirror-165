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

extras_require = \
{':python_full_version >= "3.7.0" and python_full_version < "3.8.0"': ['typing-extensions>=4.3.0,<5.0.0']}

setup_kwargs = {
    'name': 'pyeurlex',
    'version': '0.2.0',
    'description': 'This is a python module to create SPARQL queries for the EU Cellar repository, run them and subsequently download their data. Notably, it directly supports all resource types.',
    'long_description': '# pyeurlex package\n\nThis is a python module to create SPARQL queries for the EU Cellar repository, run them and subsequently download their data. Notably, it directly supports all resource types. Some parts like the SPARQL queries are based on the R-based [eurlex](https://github.com/michalovadek/eurlex) package by Michal Ovadek, but then I wanted one for python and was not satisfied with existing python packages.\n\n## Usage\n\nImport and instantiate the moduel\n\n```\nfrom eurlex import Eurlex\neur = Eurlex()\n```\n\nThen you can construct you query. (or alternatively you can use your own or one constructed via the wizard https://op.europa.eu/en/advanced-sparql-query-editor\n\n```\nq = eur.make_query(resource_type = "caselaw", order = True, limit = 10)\nprint(q)\n```\n\nFinally, you can run this query.\n\n```\nd = eur.query_eurlex(q)  # where q is a query generated in a previous step or a string defined by you\nprint(d)\n```\nThis will return a pandas data frame of the results. Its columns depend on the the fields that you included. At the moment, not all fields are named properly in the dataframe and you will have to set their name manually if desired.\n\nOnce you pick a single url or identifier from the df, you can download a notice or data based on that indentifier. To download the notices as xml, use `download_xml()` as below.\n\n```\nx = eur.download_xml("32014R0001", notice="tree") # without the file parameter to specify the filename, the celex number will be used.\nprint(x)\n```\n\nTo get data associated with an identifier, use `get_data()`. This will return the data as a string,\n```\nd = eur.get_data("http://publications.europa.eu/resource/celex/32016R0679", type="text")\nprint(d)\n```\n\n# Why another package/module?\n\nWhile there was already the R packages by Michal Ovadek, I wanted a python implementation.\nThere is also https://github.com/seljaseppala/eu_corpus_compiler but that also only does regulatory/legislative documents. Additionally, there is https://pypi.org/project/eurlex/, but it for example does not have a way to generate SPARQL queries and is also very focused on legislation. In addition, while internally it uses SPARQL and cellar as well, its documentation is focused on accessing and processing documents via CELEX number, which is not really helpful to me. Another one is https://github.com/Lexparency/eurlex2lexparency which also seems to focus on legislative documents and \n',
    'author': 'step21',
    'author_email': 'step21@devtal.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
