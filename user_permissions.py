import requests
import os
import json
import urllib.parse
from dotenv import load_dotenv

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
    
auth = (USERNAME, ACCESS_TOKEN)

def search_url(JIRA_URL):
    searchType = input("Select type of search (username/email/name:").strip().lower()

    if searchType not in ["username", "email", "name"]:
        print(f"What's {searchType}!")
        return
    elif searchType == "username":
        getUser = input(f"{searchType}: ")
        parsedQuery = urllib.parse.quote(getUser)
        url = f"{JIRA_URL}/rest/api/2/user?username={parsedQuery}&expand=groups"
    elif searchType == "email" or searchType == "name":
        getUser = input(f"{searchType}: ")
        parsedQuery = urllib.parse.quote(getUser)
        url = f"{JIRA_URL}/rest/api/2/user/picker?query={parsedQuery}"
    else:
        print("FAIL!")
        return
    
    return url

# def get_groups(url,):


def get_response(HEADERS, JIRA_URL):
    url = search_url(JIRA_URL)
    try:
        response = requests.get(
            url = url,
            headers=HEADERS,
            )
        response.raise_for_status()
        theUser = response.json()
        if theUser:
            return json.dumps(theUser, indent = 2)
    except requests.exceptions.RequestException as e:
        print(f"Error getting : {e}")

print(get_response(HEADERS, JIRA_URL))