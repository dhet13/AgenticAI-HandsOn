# 📰 Vertex AI ADK 기반 News Agent 초기 배포 및 실행 절차

이 문서는 Google Cloud Vertex AI의 **ADK (Agent Development Kit)** 를 활용하여  
News Agent를 처음으로 **배포(deploy)** 하고 **테스트 실행(stream query)** 하기 위한 전체 절차를 정리한 것입니다.

---

## ✅ 0. 사전 준비

### 0.1 Vertex AI API & Cloud Resource Manager API 활성화

프로젝트 대시보드에서 아래 API를 반드시 활성화해야 합니다.

- Vertex AI API  
- Cloud Resource Manager API  

터미널에서도 가능:
```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

---

## ✅ 1. 환경 구성

### 1.1 Python 패키지 버전 고정 (requirements.txt)

Google ADK와 Vertex AI SDK는 버전 호환성이 중요합니다.  
아래와 같이 `requirements.txt` 파일을 생성하세요.

```bash
# requirements.txt
google-cloud-aiplatform[adk,agent_engines]==1.126.1
google-adk==1.15.1
google-cloud-storage>=2.18.0,<3.0.0

# Session serialization & runtime safety
pydantic==2.11.7
cloudpickle==3.1.2

protobuf>=5.26.1,<6
```

설치 명령:
```bash
pip install -r requirements.txt
```

---

## ✅ 2. 인증 설정

### 2.1 gcloud 계정 활성화 확인
```bash
gcloud auth list
```

출력 예시:
```
Credentialed Accounts
ACTIVE: *
ACCOUNT: nlp.ysheo419@gmail.com
```

TODO: ACCOUNT 활성화를 위해 본인 계정 메일주소로 set 
```bash
gcloud config set account nlp.ysheo419@gmail.com
```

---

### 2.2 프로젝트 ID 및 리전 설정

Cloud Shell 또는 Vertex Workbench 터미널에서:
```bash
gcloud config set project project-test-2-477511
gcloud config set compute/region asia-northeast1
```

---

### 2.3 서비스 계정 권한 확인

Vertex AI Reasoning Engine용 서비스 계정이 버킷에 접근 가능해야 합니다.  

1) 버킷(데이터, 모델 저장소) 만들기
    * TODO: 버킷 이름은 다르게! + unique!  
    * 아래 예시에서의 버킷 이름: adk-agent-deploy-bucket-ysh-tokyo-v2

    ```bash
    gsutil mb -l asia-northeast1 gs://adk-agent-deploy-bucket-ysh-tokyo-v2
    ```

2) project 번호 조회 --> 자주 사용됨 (project_key라고 부르겠음): `기록해둘것!!!` 
    * 우리가 사용하는 PROJECT_ID 컴퓨터는 다른 숫자 포멧으로 처리함. 
    * 예를 들어, 우리는 PROJECT_ID가 `project-test-2-477511`로 알고 있지만,  
    컴퓨터는 `542290598419`로 처리함. 둘은 같은 의미지만 표현만 다름  

    ```bash 
    gcloud projects describe PROJECT_ID --format="value(projectNumber)"
    ```

    예시 
    ```bash 
    gcloud projects describe project-test-2-477511 --format="value(projectNumber)"
    ```

3) setup_bucket.sh 파일 수정하기 (개인 세팅으로)
* PROJECT_ID="{개인 project ID}"      e.g. "my-instance-ysh-4"
* PROJECT_NUMBER="{개인 project_key}"   e.g. "549357202415"
* BUCKET={개인 버킷 이름}           e.g. "gs://adk-agent-deploy-bucket-ysh-tokyo-v2"


4) setup_bucket.sh 파일 실행하기 
    ```bash
    bash setup_bucket.sh
    ```

---

## ✅ 3. 에이전트 엔진 배포 (Deploy)

### 3.1 배포 명령 실행

```bash
adk deploy agent_engine shared_news_agent \
  --project="{본인 프로젝트 ID}" \
  --region="{본인 region}" \
  --staging_bucket="gs://{본인 bucket명}" \
  --display_name="{본인 API 이름}"
```


* 예시 
```bash
adk deploy agent_engine shared_news_agent \
  --project="my-instance-ysh-4" \
  --region="asia-northeast1" \
  --staging_bucket="gs://adk-agent-deploy-bucket-ysh-tokyo-v2" \
  --display_name="google_news_agent_v1"
```

> ⚠️ 참고:  
> `--location` 대신 `--region` 옵션을 사용해야 합니다.  
> `--staging_bucket`(밑줄 `_`)도 정확히 입력해야 합니다.

---

### 3.2 성공 메시지 예시

```
AgentEngine created. Resource name:
projects/542290598419/locations/asia-northeast1/reasoningEngines/{에이전트 고유 ID}
```
* 예시 

```
AgentEngine created. Resource name:
projects/542290598419/locations/asia-northeast1/reasoningEngines/7096670258131369984
```

이 리소스 이름이 바로 **에이전트의 고유 ID**입니다.

---

## ✅ 4. 쿼리 테스트 (Stream Query)

### 4.1 세션 생성 (Session 생성)
```bash
ACCESS_TOKEN="$(gcloud auth print-access-token)"

curl -sS -X POST \
 -H "Authorization: Bearer ${ACCESS_TOKEN}" \
 -H "Content-Type: application/json" \
 "https://asia-northeast1-aiplatform.googleapis.com/v1/projects/{PROEJCT_ID}/locations/{지역}/reasoningEngines/{에이전트고유번호}:query" \
 -d '{
       "class_method": "create_session",
       "input": { "user_id": "testId" }
     }'

```
예시
```bash
ACCESS_TOKEN="$(gcloud auth print-access-token)"

curl -sS -X POST \
 -H "Authorization: Bearer ${ACCESS_TOKEN}" \
 -H "Content-Type: application/json" \
 "https://asia-northeast1-aiplatform.googleapis.com/v1/projects/project-test-2-477511/locations/asia-northeast1/reasoningEngines/7096670258131369984:query" \
 -d '{
       "class_method": "create_session",
       "input": { "user_id": "testId" }
     }'
```

성공 시, JSON 응답에 `"id": "세션ID값"` 이 포함됩니다.

---

### 4.2 스트리밍 쿼리 실행

세션 ID를 이용해 다음 명령을 실행합니다:

```bash
ACCESS_TOKEN="$(gcloud auth print-access-token)"
SESSION_ID="세션_ID_여기에_입력"

curl -N \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://asia-northeast1-aiplatform.googleapis.com/v1/projects/{PROEJCT_ID}/locations/{지역}/reasoningEngines/{에이전트고유번호}:streamQuery?alt=sse" \
  -d "{
        \"class_method\": \"stream_query\",
        \"input\": {
          \"user_id\": \"testId\",
          \"session_id\": \"${SESSION_ID}\",
          \"message\": \"Top Korea news today: 5 bullets.\"
        }
      }"
```


> ✅ 성공 시, 실시간으로 뉴스 요약 텍스트가 출력됩니다.  
> Grounding metadata에는 실제 뉴스 출처 도메인 (예: `apnews.com`, `koreaherald.com`)이 포함됩니다.

---

## ✅ 5. Python SDK로 실행

### 5.1 `stream_test.py` 예시 코드

```python
# stream_test.py
import vertexai
from vertexai import agent_engines

PROJECT = "project-test-2-477511"       # 본인꺼 
LOCATION = "asia-northeast1"            # 본인꺼 

# 본인꺼로! 
# ENGINE = (
#    "projects/{PROJECT_ID}/locations/{리전}/"
#    "reasoningEngines/에이전트고유번호"
#)
ENGINE = (
    "projects/project-test-2-477511/locations/asia-northeast1/"
    "reasoningEngines/7096670258131369984"
)
USER_ID = "testId"
SESSION_ID = "<세션 ID 입력>"

vertexai.init(project=PROJECT, location=LOCATION)
eng = agent_engines.get(ENGINE)

print("🔹 Streaming response from agent...\n")

sources = set()
for event in eng.stream_query(
    user_id=USER_ID,
    session_id=SESSION_ID,
    message="Top Korea news today: 5 bullets."
):
    parts = event.get("content", {}).get("parts", [])
    for p in parts:
        txt = p.get("text")
        if txt:
            print(txt, end="", flush=True)

    meta = event.get("grounding_metadata", {})
    chunks = meta.get("grounding_chunks", [])
    for chunk in chunks:
        domain = chunk.get("web", {}).get("domain")
        if domain:
            sources.add(domain)

print("\n\n✅ Sources:")
for s in sorted(sources):
    print(" -", s)
```

실행:
```bash
python3 stream_test.py
```

---

## ✅ 6. 실행 결과 예시

```
🔹 Streaming response from agent...

Here's a summary of the top news from Korea:
• North Korea fired an unidentified ballistic missile towards the East Sea...
• Bang Si-hyuk, chairman of Hybe, questioned for unfair trading...
• Leaders concluded the APEC summit with trade truce between US and China.

✅ Sources:
 - apnews.com
 - koreaherald.com
 - koreatimes.co.kr
 - scmp.com
```

---

## ✅ 7. 오류 해결 팁

| 오류 메시지 | 원인 | 해결 방법 |
|--------------|------|------------|
| `PermissionDenied: Cloud Resource Manager API has not been used` | Cloud Resource Manager API 미활성화 | `gcloud services enable cloudresourcemanager.googleapis.com` |
| `No such option: --location` | 구버전 ADK | `--region` 사용 |
| `email field missing` | GCP 계정 활성화 필요 | `gcloud config set account <email>` |
| `Failed to create session` | 서비스 계정 권한 부족 | 버킷 IAM에 `roles/storage.objectAdmin` 추가 |
| `Extra inputs are not permitted` | ADK 버전 불일치 | ADK 및 aiplatform 버전 맞추기 (`google-adk==1.15.1`, `aiplatform==1.126.1`) |

---

## ✅ 8. Telemetry 설정 (선택사항)

경고:
```
Your 'enable_tracing=False' setting is being deprecated.
```

→ 해결: `enable_tracing` 옵션 제거 후, 환경 변수 사용
```python
agent_engines.create(
  env_vars={
    "GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY": "true"
  }
)
```

또는 콘솔에서 직접 토글  
[https://console.cloud.google.com/vertex-ai/agents](https://console.cloud.google.com/vertex-ai/agents)

---

## ✅ 9. 정리

| 구분 | 값 |
|------|----|
| **Project ID** | `project-test-2-477511` |
| **Project Number** | `542290598419` |
| **Region** | `asia-northeast1` |
| **Bucket** | `gs://adk-agent-deploy-bucket-ysh-tokyo` |
| **Agent Engine Resource** | `projects/542290598419/locations/asia-northeast1/reasoningEngines/7096670258131369984` |

---

## 📌 요약 흐름

1️⃣ 환경 구성 및 인증  
2️⃣ API 활성화  
3️⃣ ADK로 Agent Engine 배포  
4️⃣ Session 생성  
5️⃣ Stream Query 실행 (curl or Python SDK)  
6️⃣ 뉴스 요약 응답 확인 및 Source 표시  

---
