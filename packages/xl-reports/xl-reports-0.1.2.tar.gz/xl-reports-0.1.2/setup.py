# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xl_reports']
install_requires = \
['mypy>=0.971,<0.972', 'openpyxl>=3.0.10,<4.0.0']

setup_kwargs = {
    'name': 'xl-reports',
    'version': '0.1.2',
    'description': 'Generate reports from a excel file and some data.',
    'long_description': 'XL Reports\n----------\n\nGenerate Excel reports!\n\n1. Create an Excel template file\n2. Define a report configuration\n3. Fetch your data\n4. Generate report\n\n\n## Report Configuration Schema\n\nReport configuration is defined as array/list of objects/dicts.\n\n\n**"cell"**: <string> Worksheet cell coordinates to insert data, example: `"B2"`\n\n**"range"**: <string> Worksheet coordinate range to insert data. Range start coordinate is required and end coordinate is optional. examples: `"B2:"` or `"B2:C5"`\n\n**"data_key**": <string> Key to use when fetching values from the data dictionary to insert into the worksheet. example: `data["report_date"]`\n\n**"sheet"**: <string> Worksheet name.\n\n\n**Example configuration**\n\n```\n[\n    {\n        "cell": "B2",\n        "data_key": "account",\n        "sheet": "my_sheet"\n    },\n    {\n        "cell": "B4",\n        "data_key": "report_date",\n        "sheet": "my_sheet"\n    },\n    {\n        "range": "A8",\n        "data_key": "report_data",\n        "sheet": "my_sheet"\n    }\n]\n```\n\n**Example data**\n\n```\n[{\n    "account": "Engineering",\n    "report_date": str(date.today()),\n    "report_data": [\n        [23.43, 11.96, 9.66],\n        [6.99, 65.87, 45.33],\n    ]\n}]\n```',
    'author': 'Dustin Sampson',
    'author_email': 'dustin@sparkgeo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sparkgeo/xl-reports',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
