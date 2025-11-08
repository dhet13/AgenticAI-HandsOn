# stream_test.py
import vertexai
#from vertexai.preview import agent_engines
from vertexai import agent_engines


# ===== 설정 =====
PROJECT = "project-test-2-477511"
LOCATION = "asia-northeast1"
ENGINE = (
    "projects/project-test-2-477511/locations/asia-northeast1/"
    "reasoningEngines/7096670258131369984"
)
SESSION_ID = "6409550807317872640"
USER_ID = "testId"

# ===== 초기화 =====
vertexai.init(project=PROJECT, location=LOCATION)
engine = agent_engines.get(ENGINE)

# ===== 스트리밍 질의 =====
print("🔹 Streaming response from agent...\n")

sources = set()
for event in engine.stream_query(
    user_id=USER_ID,
    session_id=SESSION_ID,
    message="Top Korea news today: 5 bullets."
):
    # 텍스트 부분만 출력
    parts = event.get("content", {}).get("parts", [])
    for p in parts:
        txt = p.get("text")
        if txt:
            print(txt, end="", flush=True)

    # 소스 도메인 수집
    meta = event.get("grounding_metadata", {})
    chunks = meta.get("grounding_chunks", [])
    for chunk in chunks:
        web = chunk.get("web", {})
        domain = web.get("domain")
        if domain:
            sources.add(domain)

# ===== 결과 =====
print("\n\n✅ Sources:")
for s in sorted(sources):
    print(" -", s)
