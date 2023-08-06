# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hotjar_data_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'hotjar-data-wrapper',
    'version': '0.1.0',
    'description': 'a wrapper for using Hotjar APIs',
    'long_description': '# Hotjar Data Wrapper\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThis is a wrapper for Hotjar APIs to let you login and download survey data and metadata for your account.\n\n## Supported APIs and docs\n\n- [Hotjar Data Wrapper](#hotjar-data-wrapper)\n  - [Supported APIs and docs](#supported-apis-and-docs)\n    - [Get survey metadata](#get-survey-metadata)\n    - [Get survey questions](#get-survey-questions)\n    - [List all surveys](#list-all-surveys)\n    - [Get all survey metadata](#get-all-survey-metadata)\n\n### Get survey metadata\n\nLogin and download metadata for a specific survey.\n\n```python\nmeta = get_survey_metadata(survey_id=survey_id, site_id=site_id, username=username, password=password)\nmeta.status_code # 200\nmeta.content # prints content\n```\n\n### Get survey questions\n\nLogin and download questions for a specific survey.\n\n```python\nquestions = get_survey_questions(survey_id=survey_id, site_id=site_id, username=username, password=password)\nquestions.content \n```\n\n### List all surveys\n\nLogin and download list of all surveys for a given site ID.\n\n```python\nall_surveys = get_list_all_surveys(site_id=site_id, username=username, password=password)\nall_surveys.content\n```\n\n### Get all survey metadata\n\nLogin and download metadata for a list of surveys with survey IDs.\n\n```python\nget_all_surveys_metadata(\n    path="data/hotjar surveys",\n    surveys_list=ids,\n    site_id=site_id,\n    username=username,\n    password=password,\n)\n```',
    'author': 'Tobias McVey',
    'author_email': 'tobias.mcvey@nav.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/navikt/hotjar-data-wrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
