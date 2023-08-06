# %%
import json
import requests

# %%
def login_hotjar(username: str, password: str):
    """
    Log into Hotjar
    """
    session = requests.Session()
    login_url = "https://insights.hotjar.com/api/v2/users"
    auth = json.dumps(
        {"action": "login", "email": username, "password": password, "remember": True}
    )
    content_type = "application/json"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36"
    headers = {"Content-Type": content_type, "user-agent": user_agent}
    session.headers = headers
    try:
        response = session.post(login_url, data=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    print(f"You are now logged in")
    return response


# %%
def get_survey_metadata(survey_id: str, site_id: str, username: str, password: str):
    """
    Log into Hotjar and download metadata for a survey. Returns a requests object with the metadata.

    The requests object contains questions, response options and question type, f.ex radio-button
    """
    session = requests.Session()
    login_url = "https://insights.hotjar.com/api/v2/users"
    auth = json.dumps(
        {"action": "login", "email": username, "password": password, "remember": True}
    )
    content_type = "application/json"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36"
    headers = {"Content-Type": content_type, "user-agent": user_agent}
    session.headers = headers
    try:
        response = session.post(login_url, data=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    try:
        data = session.get(
            f"https://insights.hotjar.com/api/v1/sites/{site_id}/polls/{survey_id}",
            timeout=120,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    print(f"Downloaded survey {survey_id}")
    return data


# %%
def get_survey_questions(survey_id: str, site_id: str, username: str, password: str):
    """
    Get all questions for a specific survey in Hotjar.
    """
    session = requests.Session()
    login_url = "https://insights.hotjar.com/api/v2/users"
    auth = json.dumps(
        {"action": "login", "email": username, "password": password, "remember": True}
    )
    content_type = "application/json"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36"
    headers = {"Content-Type": content_type, "user-agent": user_agent}
    session.headers = headers
    try:
        response = session.post(login_url, data=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    try:
        data = session.get(
            f"https://insights.hotjar.com/api/v1/sites/{site_id}/polls/{survey_id}/questions",
            timeout=120,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    print(f"Downloaded survey questions for survey {survey_id}")
    return data


# %%
def get_list_all_surveys(site_id: str, username: str, password: str):
    """
    Get a list of all surveys from Hotjar
    """
    session = requests.Session()
    login_url = "https://insights.hotjar.com/api/v2/users"
    auth = json.dumps(
        {"action": "login", "email": username, "password": password, "remember": True}
    )
    content_type = "application/json"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36"
    headers = {"Content-Type": content_type, "user-agent": user_agent}
    session.headers = headers
    try:
        response = session.post(login_url, data=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    try:
        data = session.get(
            f"https://insights.hotjar.com/api/v1/sites/{site_id}/surveys", timeout=120
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return data


# %%
def get_all_surveys_metadata(
    path: str, surveys_list: list, site_id: str, username: str, password: str
):
    """
    Download metadata for all surveys in Hotjar
    """
    session = requests.Session()
    login_url = "https://insights.hotjar.com/api/v2/users"
    auth = json.dumps(
        {"action": "login", "email": username, "password": password, "remember": True}
    )
    content_type = "application/json"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36"
    headers = {"Content-Type": content_type, "user-agent": user_agent}
    session.headers = headers
    try:
        response = session.post(login_url, data=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    response.raise_for_status()
    json_response = response.json()
    print("JSON Response")
    for key, value in json_response.items():
        print(key, ":", value, "\n")
    while response.status_code:
        for survey_id in surveys_list:
            download_url = (
                f"https://insights.hotjar.com/api/v1/sites/{site_id}/polls/{survey_id}"
            )
            print(f"Downloading survey {survey_id}")
            file_download = session.get(download_url, headers=headers, timeout=120)
            file_download.raise_for_status()
            survey_data = f"{path}/survey_{survey_id}.json"
            with open(survey_data, "w") as f:
                json.dump(file_download.text, f, ensure_ascii=False)
    return survey_data
