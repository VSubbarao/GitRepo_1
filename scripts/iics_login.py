import os
import requests
import json
import sys

# The base URL for the Informatica Cloud login API.
# This should be updated to match your region (e.g., us-east-1, eu-central-1).
BASE_URL = "https://dm-us.informaticacloud.com/ma/api/v2/user/login"

def login():
    """
    Logs into Informatica Cloud and returns a session token.
    """
    print("Attempting to log into Informatica Cloud...")

    username = os.environ.get("IICS_USER")
    password = os.environ.get("IICS_PASSWORD")

    if not username or not password:
        print("Error: IICS_USER and IICS_PASSWORD environment variables must be set.")
        sys.exit(1)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "@type": "login",
        "username": username,
        "password": password
    }

    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        session_id = data.get("sessionId")
        server_url = data.get("serverUrl")

        if not session_id or not server_url:
            print("Error: Could not retrieve session ID or server URL from login response.")
            sys.exit(1)

        print("Successfully logged in.")
        # We will need both the session ID and the server URL for subsequent requests.
        # We can print them in a format that's easy to parse by a shell script.
        print(f"SESSION_ID={session_id}")
        print(f"SERVER_URL={server_url}")

        return session_id, server_url

    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    login()
