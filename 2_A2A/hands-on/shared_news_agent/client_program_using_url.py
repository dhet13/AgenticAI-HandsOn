import json
import requests
from google.auth import default
from google.auth.transport.requests import Request

# Get default credentials and access token
creds, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds.refresh(Request())
access_token = creds.token

# API endpoint for session creation
#url_session = "https://<your-region>-aiplatform.googleapis.com/v1/projects/<your-projectid>/locations/<your-region>/reasoningEngines/<your-adent-id>:query"
project_id = "project-test-2-477511"
location = "asia-northeast3"
agent_id = "google_news_agent_v2"  # This should match your agent's display name

url_session = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/reasoningEngines/{agent_id}:query"

# Payload for session creation
payload_session = {
    "class_method": "create_session",
    "input": {
        "user_id": "testId"
    }
}

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# POST request
response = requests.post(url_session, headers=headers, data=json.dumps(payload_session))

if response.status_code == 200:
    data = response.json()
    session_id = data["output"]["id"]
    print(f"Session created successfully! Session ID: {session_id}")
else:
    print(f"Request failed ({response.status_code}):")
    print(response.text)

payload_query = {
    "class_method": "async_stream_query",
    "input": {
        "user_id": "testId",
        "session_id": session_id,
        "message": "What is the top news today"
    }
}

#url_query = "https://<your-region>-aiplatform.googleapis.com/v1/projects/<your-projectid>/locations/<your-region>/reasoningEngines/<your-adent-id>:streamQuery?alt=sse"
url_query = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/reasoningEngines/{agent_id}:streamQuery?alt=sse"
"""
with requests.post(url_query, headers=headers, data=json.dumps(payload_query), stream=True) as response:
    print("Status:", response.status_code)
    if response.status_code != 200:
        print("Error:", response.text)
    else:
        print("Streaming response:\n")
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                print(decoded_line)

"""
response = requests.post(url_query, headers=headers, data=json.dumps(payload_query))
import json
data = json.loads(response.text)

# Extract the text safely
text = data.get("content", {}).get("parts", [{}])[0].get("text", "")

print("\nAgent Response:\n")
print(text)