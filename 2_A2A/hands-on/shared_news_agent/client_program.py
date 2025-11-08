import vertexai
from vertexai import agent_engines

# Load environment variables and initialize Vertex AI
#load_dotenv()

#Project_id = '<your-project-id>'
Project_id = 'project-test-2-477511'
#Location = '<your-region>'
Location = "asia-northeast1"
app_name = "google_news_agent_v4"


# Initialize Vertex AI with the correct project and location
vertexai.init(
    project=Project_id,
    location=Location,
)

ae_apps = list(agent_engines.list())
for agent in ae_apps:
    print(f"Found agent: {agent.display_name}")

remote_app = next((a for a in ae_apps if a.display_name == app_name), None)



# Get a session for the remote app
remote_session = remote_app.create_session(user_id="U_456")

transcript_to_summarize = "what is the latest news today"

# Run the agent with this hard-coded input
response = remote_app.stream_query(
    user_id="U_456",
    session_id=remote_session["id"],
    message=transcript_to_summarize,
)

# Print responses
for event in response:
    for part in event["content"]["parts"]:
        if "text" in part:
            response_text = part["text"]
            print(f"Agent response: {response_text}")