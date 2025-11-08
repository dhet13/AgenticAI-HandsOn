#!/bin/bash
#
## 0) 변수 세팅
PROJECT_ID="my-instance-ysh-4"
PROJECT_NUMBER="549357202415"
BUCKET="gs://adk-agent-deploy-bucket-ysh-tokyo-v2"

# 1) API 활성화 (idempotent)
gcloud services enable aiplatform.googleapis.com storage.googleapis.com --project="$PROJECT_ID"

# 2) Vertex AI 서비스 에이전트 생성/확보 (idempotent)
#    생성이 이미 되어있으면 OK, 없으면 지금 만듭니다.
gcloud beta services identity create \
  --service=aiplatform.googleapis.com \
  --project="$PROJECT_ID"

# 3) 에이전트 이메일 확인 (정식 도메인: gcp-sa-aiplatform.iam.gserviceaccount.com)
SA_EMAIL="service-$PROJECT_NUMBER@gcp-sa-aiplatform.iam.gserviceaccount.com"
echo "$SA_EMAIL"

# 4) 버킷에 ObjectAdmin 부여
gsutil iam ch \
  serviceAccount:$SA_EMAIL:roles/storage.objectAdmin \
  "$BUCKET"

# (선택) Online Prediction까지 쓸 때는 온라인 예측용 에이전트에도 같은 권한을 주면 편합니다.
OP_SA="service-$PROJECT_NUMBER@gcp-sa-vertex-op.iam.gserviceaccount.com"
gsutil iam ch \
  serviceAccount:$OP_SA:roles/storage.objectAdmin \
  "$BUCKET"

# 5) 적용 확인
gsutil iam get "$BUCKET" | grep -E "$PROJECT_NUMBER|storage.objectAdmin" -n

