# agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService  # ⬅ 추가
from dotenv import load_dotenv

load_dotenv()

session_service = InMemorySessionService()  # ⬅ 세션을 메모리에 저장 (GCS 미사용)

root_agent = LlmAgent(
    name="google_news_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a news assistant that finds the latest information on the web and returns a concise, factual summary.\n"
        "Rules:\n"
        "1) Use Google Search tool to gather recent coverage (past 24–72 hours when possible).\n"
        "2) Prioritize reputable sources; avoid speculation.\n"
        "3) Deduplicate overlapping stories.\n"
        "4) If nothing reliable is found, say so.\n"
        "Output: Title / 3–5 bullets (with source domain) / Timestamp / Sources list.\n"
    ),
    description="Fetch recent news and return a short, source-backed summary.",
    tools=[google_search]
)



######################################
"""
#from google.adk.agents import Agent
from google.adk.agents import LlmAgent  # 1. 'Agent'를 'LlmAgent'로 변경
from google.adk.tools import google_search
from dotenv import load_dotenv

load_dotenv()

# Define the agent
#root_agent = Agent(
root_agent = LlmAgent(  # 2. 여기도 'LlmAgent'로 변경
    name="google_news_agent",
    model="gemini-2.5-flash",
    instruction="Look for all the latest news in the internet and provide a crisp summary based on the topic",
    description="An agent that uses Google Search to fetch up-to-date news",
    tools=[google_search],  # Built-in Google Search tool
)
"""
