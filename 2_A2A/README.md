# Part 2. A2A 프로토콜 및 다중 에이전트 협업 

* 강의 시작 전 진행 방향을 위한 사전 설문조사 입니다. 참여부탁드립니다. (1분) 
👉 [Google Form 바로 가기](https://forms.gle/pnA3swLqHY2GNEUh8)

# 🗓️ 2차시 교육 커리큘럼: A2A 협업 및 Agentic AI 구축

## **📘 교육 목표:**
-   **[Analytic Agent 구축]** **기계 학습 기반의 고성능 AI 분석 전문가** 모델을 Vertex AI 환경에서 빠르게 재구축하고 **Tool API**로 배포한다.
-   **[Manager Agent 설계]** **Agentic AI**의 핵심 원리(계획, Tool 사용)를 이해하고, **Gemini API**를 활용하여 **AI 매니저 에이전트**를 구축한다.
-   **[A2A 협업 구현]** **AI 분석 전문가**의 API를 **Tool**로 연결하여, **A2A(Agent-to-Agent) 협업 워크플로우**를 완성한다.
-   **[Intelligent Workflow]** 사용자의 모호한 자연어 요청을 AI가 **능동적인 질문(Slot Filling)**을 통해 정형 데이터로 변환하는 **'지능형 면접관'** 시스템을 완성한다.

---

## ⏰ 시간표 (총 6 세션, 15분 휴식)

| 세션 | 시간 | 내용 |
| :--- | :--- | :--- |
| **Session 1** | **09:30 – 10:20** (50분) | 전체 Overview 및 Agentic AI 환경 구축 |
| 휴식 | 10:20 – 10:35 (15분) | |
| **Session 2** | **10:35 – 11:25** (50분) |  ML 대출 심사 모델 구축 및 '배포 시작' |
| 휴식 | 11:25 – 11:40 (15분) | |
| **Session 3** | **11:40 – 12:30** (50분) | Gemini에 'AI 심사관 API'를 Tool로 정의하기 |
| **점심 식사** | **12:30 – 13:30** (60분) | *(Endpoint 배포 완료 대기)* |
| **Session 4** | **13:30 – 14:20** (50분) | 첫 A2A 협업 구현 (Function Calling 테스트) |
| 휴식 | 14:20 – 14:35 (15분) | |
| **Session 5** | **14:35 – 15:25** (50분) | '지능형 면접관' 설계 및 정보 수집 루프 구현 |
| 휴식 | 15:25 – 15:40 (15분) | |
| **Session 6** | **15:40 – 16:30** (50분) | 최종 파이프라인 완성 및 E2E 테스트 |

---
<br>

# 📚 세션별 상세 내용


## Session 1: 전체 Overview 및 Agentic AI 환경 구축 (09:30 – 10:20)

### 🎯 학습 목표
- 전체 프로젝트의 아키텍처(A2A 협업)를 이해합니다.
- Agentic AI의 핵심 개념(계획, 도구 사용)을 학습합니다.
- Gemini API를 사용하기 위한 Vertex AI SDK 환경을 구축합니다.

### 🧠 이론 및 개념
1.  **전체 Overview:** 클라우드(Vertex AI) 기반 ML 전문가 모델 + LLM 매니저를 통합한 멀티 에이전트 구조 이해.
2.  **Agentic AI의 이해:** 단순 챗봇 vs 자율 에이전트 (계획, 도구 사용, 상태 관리).
3.  **A2A 협업 모델:** LLM(소통/추론)과 ML(정밀예측)의 역할 분담과 연결 필요성.

### 🛠️ 실습 (Vertex AI Notebook)
1.  `Session 2`를 위한 새 Jupyter Notebook 생성.
2.  **SDK 설치 및 업데이트:** `!pip install google-cloud-aiplatform xgboost --upgrade`
3.  **환경 초기화:** `aiplatform.init(project=PROJECT_ID, location=REGION)` 설정.
4.  **Gemini 모델 로드 및 테스트:** `GenerativeModel("gemini-pro")` 객체 생성 및 간단한 추론 테스트.

***

## Session 2: 기계학습(ML) 기반 대출 심사 모델 구축 및 배포 (10:35 – 11:25)

### 🎯 학습 목표
- 전문가 확보를 위한 ML 모델 구축 전 과정을 **압축 실행**하여 전문가 API를 생성합니다.
- Endpoint 배포를 **'시작'**하고, 백그라운드에서 배포가 진행되도록 합니다.

### 🧠 이론 및 개념
1.  **ML 기반 전문가 모델 구축:** 데이터 로드 → 전처리 → 학습(XGBoost) → 저장(GCS) → 등록(Registry) → 배포(Endpoint)의 6단계를 빠르게 복습합니다.
2.  **비동기 배포:** Endpoint 배포는 15-20분이 소요되며, 이 시간 동안 다른 작업을 할 수 있음을 안내합니다.

### 🛠️ 실습 (제공된 Fast-Track Notebook 실행)
1.  **[제공된 노트북 실행]** 전문가 모델 학습 코드가 담긴 노트북을 제공받습니다.
2.  **변수 설정:** 수강생 각자의 `PROJECT_ID`, `BUCKET_NAME`을 입력합니다.
3.  **전체 셀 실행:** 'Run All Cells' 또는 Shift+Enter로 모든 단계를 실행합니다.
    -   (데이터 로드, XGBoost 학습, GCS 업로드, Model Registry 등록이 자동으로 수행됨)
4.  **배포 시작:** 마지막 셀에서 `model.deploy(...)` (SDK 사용) 또는 UI를 통해 Endpoint 배포를 **"시작"**합니다.
5.  **GCP 콘솔 확인:** Endpoint가 '만드는 중...' 상태임을 확인하고 **기다리지 않고 바로 다음 세션으로 넘어갑니다.**

***

## Session 3: Gemini에 'AI 심사관 API'를 Tool로 정의하기 (11:40 – 12:30)

### 🎯 학습 목표
- (Endpoint가 백그라운드에서 배포되는 동안) Gemini가 사용할 수 있도록 'AI 대출 심사 API'의 **Tool 스키마**를 Python 코드로 정의합니다.

### 🧠 이론 및 개념
1.  **Function Calling 원리:** LLM에게 API의 '사용 설명서'를 제공하는 방법.
2.  **Tool 스키마 설계:** 전문가 모델의 모든 피처(Features)를 JSON Schema 파라미터로 명시하는 방법.

### 🛠️ 실습 (Session 1 노트북에서 계속)
1.  `Tool` 및 `FunctionDeclaration` 클래스 임포트.
2. 학습된 `model_features.pkl` 파일을 **다운로드**하여 피처 리스트를 로드합니다.
3.  이 피처 리스트를 기반으로 `check_loan_approval` 함수의 모든 파라미터를 정의하는 Python 코드 작성.
4.  정의된 `Tool` 객체를 `gemini-pro` 모델에 연결하여 초기화.
5.  *(시간이 남으면) 점심 식사 후 진행할 Session 4의 코드(A2A 호출)를 미리 리뷰합니다.*

***

## Session 4: 첫 A2A 협업 구현 (Function Calling 테스트) (13:30 – 14:20)

### 🎯 학습 목표
- (점심시간 동안 배포가 완료된) Endpoint를 사용하여 **첫 A2A 협업**을 테스트합니다.
- Gemini가 FunctionCall을 반환하면, 실제 API를 호출하고 결과를 다시 Gemini에게 피드백하는 전체 루프를 구현합니다.

### 🧠 이론 및 개념
1.  **추론 및 실행(Reasoning & Action) Cycle:** LLM의 결정 → 코드 실행 → LLM의 피드백의 3단계 워크플로우.
2.  **A2A 호출 함수 구현:** `Endpoint.predict()` 코드를 재활용하여 API 호출 함수를 정의.

### 🛠️ 실습 (One-Shot Prediction)
1.  **Endpoint 상태 확인:** GCP 콘솔에서 Endpoint가 '활성' 상태인지 확인. (Endpoint ID 복사)
2.  **A2A 호출 함수 구현:** `FunctionCall` 객체를 받아 전문가 모델의 Endpoint API를 호출하는 `call_loan_api(...)` 함수 작성.
3.  **테스트 프롬프트 작성:** (정보가 모두 포함된) 상세한 대출 요청 프롬프트 작성.
4.  **전체 루프 실행:**
    -   `model.generate_content(...)` 호출 → `FunctionCall` 획득.
    -   `call_loan_api(...)` 호출 → API 예측 결과(`[0]` 또는 `[1]`) 획득.
    -   API 결과를 다시 Gemini에게 전달 → "심사 결과, 승인/거절입니다." 최종 자연어 답변 획득.

***

## Session 5: '지능형 면접관' 설계 및 정보 수집 루프 구현 (14:35 – 15:25)

### 🎯 학습 목표
- 사용자의 모호한 요청에 대해 AI가 능동적으로 정보를 수집(Slot Filling)하도록 **시스템 프롬프트**를 설계하고, **대화 루프**를 구현합니다.

### 🧠 이론 및 개념
1.  **Slot Filling:** 정해진 '슬롯'(API 파라미터)을 채우기 위해 대화를 주도하는 AI 기술.
2.  **대화 상태 관리:** 수집된 정보(`collected_data` 딕셔너리)를 Python 코드로 추적하는 방법.

### 🛠️ 실습 (Slot Filling Loop)
1.  `model.start_chat()`으로 채팅 세션 초기화 및 **'지능형 면접관' 시스템 프롬프트** 주입.
2.  `collected_data = {}` 딕셔너리 정의.
3.  `while True:` 루프를 사용하여, Gemini의 질문과 사용자의 답변을 주고받는 대화형 인터페이스 구현.
4.  사용자 답변을 파싱하여 `collected_data`에 저장.
5.  Gemini가 **"모든 정보가 수집되었습니다."**와 같은 종료 키워드를 반환하면 루프를 `break`하는 로직 구현.

***

## Session 6: 최종 파이프라인 완성 및 E2E 테스트 (15:40 – 16:30)

### 🎯 학습 목표
- Session 5에서 수집된 최종 데이터를 전문가 모델 API 형식에 맞게 전처리하고, A2A 협업을 실행합니다.
- '지능형 면접관'부터 '최종 심사 결과'까지의 End-to-End 파이프라인을 완성하고 시연합니다.

### 🧠 이론 및 개념
1.  **E2E(End-to-End) 파이프라인:** 사용자 입력 → 질문 → 데이터 수집 → 전처리 → A2A 호출 → 최종 응답의 전체 흐름 통합.
2.  **데이터 무결성:** 수집된 자연어 데이터를 API가 요구하는 정형 데이터(원-핫 인코딩 등)로 최종 변환.

### 🛠️ 실습 (파이프라인 통합)
1.  Session 5의 대화 루프가 종료되면, `collected_data` 딕셔너리를 **전문가 모델 모델의 전처리 함수**에 연결.
2.  전처리된 데이터를 Session 4의 **A2A 호출 함수(`call_loan_api`)**에 전달.
3.  API 결과를 다시 Gemini에게 전달하여 **최종 자연어 답변** 생성.
4.  **종합 시연:** Notebook을 처음부터 실행하여, "대출 받고 싶어요"라는 첫마디부터 최종 심사 결과가 나올 때까지의 전체 과정을 시연 및 검증.
