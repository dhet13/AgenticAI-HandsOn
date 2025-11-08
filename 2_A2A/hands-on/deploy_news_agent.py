import os
from absl import app, flags
from dotenv import load_dotenv

import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

# 너의 에이전트 정의를 가져온다 (LlmAgent + google_search)
# shared_news_agent/agent.py 안의 root_agent를 임포트하는 경로로 수정
from shared_news_agent.agent import root_agent

import datetime
import os

FLAGS = flags.FLAGS
flags.DEFINE_string("project_id", None, "GCP Project ID (e.g., project-test-2-477511)")
flags.DEFINE_string("location", None, "GCP Region (e.g., asia-northeast1)")
flags.DEFINE_string("bucket", None, "GCS Bucket name (no gs:// prefix)")

flags.DEFINE_bool("list", False, "List all agent engines")
flags.DEFINE_bool("create", False, "Create new agent engine")
flags.DEFINE_bool("delete", False, "Delete an agent engine")
flags.DEFINE_string("resource_id", None, "ReasoningEngine resource name")
flags.mark_bool_flags_as_mutual_exclusive(["create", "delete"])



def create() -> None:
    """Creates an agent engine for News Agent."""
    adk_app = AdkApp(agent=root_agent, enable_tracing=True)

    # ✅ Display name 자동 생성 (버전 태깅)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    display_name = os.getenv("DISPLAY_NAME", f"{root_agent.name}_{timestamp}")

    remote_agent = agent_engines.create(
        adk_app,
        display_name=display_name,
        requirements=[
            "google-adk (>=1.15.1)",
            "google-cloud-aiplatform[agent_engines] (>=1.126.1)",
            "pydantic (>=2.11.7,<3.0.0)",
            "cloudpickle (>=3.1.2)",
        ],
    )

    print(f"Created remote agent: {remote_agent.resource_name}")
    print(f"Display name: {display_name}")



def delete(resource_id: str) -> None:
    remote = agent_engines.get(resource_id)
    remote.delete(force=True)
    print(f"DELETED: {resource_id}")

def list_agents() -> None:
    agents = agent_engines.list()
    for a in agents:
        print(f"{a.display_name} | {a.name} | created={a.create_time}")

def main(argv):
    del argv
    load_dotenv()

    project_id = FLAGS.project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    location   = FLAGS.location   or os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket     = FLAGS.bucket     or os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")

    if not project_id or not location or not bucket:
        raise SystemExit("project_id / location / bucket 설정이 필요합니다 (.env 또는 플래그).")

    # staging_bucket은 gs:// 프리픽스 필요
    vertexai.init(project=project_id, location=location, staging_bucket=f"gs://{bucket}")

    if FLAGS.list:
        list_agents()
    elif FLAGS.create:
        create()
    elif FLAGS.delete:
        if not FLAGS.resource_id:
            raise SystemExit("--resource_id 필요")
        delete(FLAGS.resource_id)
    else:
        print("사용법: --create | --list | --delete --resource_id=...")

if __name__ == "__main__":
    app.run(main)
