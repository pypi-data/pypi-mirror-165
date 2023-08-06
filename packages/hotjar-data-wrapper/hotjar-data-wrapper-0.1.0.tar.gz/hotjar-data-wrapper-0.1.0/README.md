# Hotjar Data Wrapper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a wrapper for Hotjar APIs to let you login and download survey data and metadata for your account.

## Supported APIs and docs

- [Hotjar Data Wrapper](#hotjar-data-wrapper)
  - [Supported APIs and docs](#supported-apis-and-docs)
    - [Get survey metadata](#get-survey-metadata)
    - [Get survey questions](#get-survey-questions)
    - [List all surveys](#list-all-surveys)
    - [Get all survey metadata](#get-all-survey-metadata)

### Get survey metadata

Login and download metadata for a specific survey.

```python
meta = get_survey_metadata(survey_id=survey_id, site_id=site_id, username=username, password=password)
meta.status_code # 200
meta.content # prints content
```

### Get survey questions

Login and download questions for a specific survey.

```python
questions = get_survey_questions(survey_id=survey_id, site_id=site_id, username=username, password=password)
questions.content 
```

### List all surveys

Login and download list of all surveys for a given site ID.

```python
all_surveys = get_list_all_surveys(site_id=site_id, username=username, password=password)
all_surveys.content
```

### Get all survey metadata

Login and download metadata for a list of surveys with survey IDs.

```python
get_all_surveys_metadata(
    path="data/hotjar surveys",
    surveys_list=ids,
    site_id=site_id,
    username=username,
    password=password,
)
```