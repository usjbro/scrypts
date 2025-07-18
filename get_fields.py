import requests
import os
import json
import urllib.parse
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "test").lower()
print(f"Environment {ENVIRONMENT}")

ACCESS_TOKEN = os.getenv("TEST_TOKEN") if ENVIRONMENT == "test" else os.getenv("PROD_TOKEN")
JIRA_URL = os.getenv("TEST_URL") if ENVIRONMENT == "test" else os.getenv("PROD_URL")
USERNAME = os.getenv("USERNAME")
print(f"URL: {JIRA_URL}")

HEADERS = {"Accept": "application/json",
           "Content-Type": "application/json",
           "Authorization": f"Bearer {ACCESS_TOKEN}"}
    
auth = ("username", ACCESS_TOKEN)

def get_fields():
    url = f"{JIRA_URL}/rest/api/2/field"
    response = requests.get(
        url=url,
        headers=HEADERS,
    )
    if response.status_code == 200:
        allFields = []
        theFields = response.json()
        response.raise_for_status()  # Raise exception for HTTP error codes
        for field in theFields:
            fields = {
            "id": field.get("id"),
            "name": field.get("name"),
            "custom": field.get("custom"),
            "orderable": field.get("orderable"),
            "navigable": field.get("navigable"),
            "searchable": field.get("searchable")
            }
            allFields.append(fields)
            print(f"id: {fields['id']}\nname: {fields['name']}\ncustom: {fields['custom']}\norderable: {fields['orderable']}\nnavigable: {fields['navigable']}\nsearchable: {fields['searchable']}\n")

            df = pd.DataFrame(allFields)
            df.to_csv('prod_fields.csv', index=False)
    else:
        print(f"Error getting {response.status_code}")

get_fields()