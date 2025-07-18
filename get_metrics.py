import csv
import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "test").lower()
print(f"Environment {ENVIRONMENT}")

ACCESS_TOKEN = os.getenv("TEST_TOKEN") if ENVIRONMENT == "test" else os.getenv("PROD_TOKEN")
print(ACCESS_TOKEN)
JIRA_URL = os.getenv("TEST_URL") if ENVIRONMENT == "test" else os.getenv("PROD_URL")
USERNAME = os.getenv("USERNAME")
print(f"URL: {JIRA_URL}")

HEADERS = {"Accept": "application/json",
           "Content-Type": "application/json",
           "Authorization": f"Bearer {ACCESS_TOKEN}"
           }
    
auth = ("BROWJ696", ACCESS_TOKEN)

jql = 'project = "User Management" AND status = Done and assignee = BROWJ696'

params = {
    'jql': jql,
    'startAt': 0,
    'maxresults': 50,
    'expand': "renderedFields",
    'fields': [
        "key", "summary", "description", "reporter", "created", "resolutiondate", "assignee", "customfield_12345"
        ]
}
url = f"{JIRA_URL}/rest/api/2/search"

response = requests.get(
        f"{JIRA_URL}/rest/api/2/search",
        headers=HEADERS,
        params=params
    )
if response.status_code == 200:  
    issues = response.json()['issues']
    response.raise_for_status()  # Raise exception for HTTP error codes
    for issue in issues:
        key = issue['key']
        summary = issue['fields']['summary']
        reporter = issue['fields']['reporter']['emailAddress']
        created = issue['fields']['created']
        resolutiondate = issue['fields']['resolutiondate']
        assignee = issue['fields']['assignee']['name']
        customfield_13605 = issue['fields']['customfield_12345']
        print(f"Key: {key}\nSummary: {summary}\nReporter: {reporter}\nCreated: {created}\nResolutiondate: {resolutiondate}\nAssignee: {assignee}\nLast Comment: {customfield_12345}")
else:
    print(f"Error getting {response.status_code}")