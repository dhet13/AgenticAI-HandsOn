# 🗓️ ADK로 구축하는 지능형 에이전트 팀

## **📘 교육 목표:**
-   **[핵심 개념]** **ADK(Agent Development Kit)**를 사용하여 에이전트의 **Tool(도구)**, **Model(모델)**, **Instruction(지시어)**을 정의하여 기능하는 에이전트를 처음부터 구축합니다.
-   **[실행]** ADK의 **Runner(실행기)**와 **SessionService(세션 관리자)**를 이해하고, 이를 통해 에이전트 상호작용을 관리 및 실행합니다.
-   **[유연성]** **LiteLLM**을 활용하여 동일한 에이전트 로직을 여러 다른 모델(Gemini, GPT, Claude)에서 실행하는 방법을 배웁니다.
-   **[Agentic AI]** 전문화된 **서브 에이전트(Sub-agent)**를 포함하는 **멀티 에이전트 팀**을 설계하고, **자동 위임(Automatic Delegation)** 기능을 구현합니다.
-   **[메모리]** **`ToolContext`** 및 **`output_key`**를 사용하여 **세션 스테이트(Session State)**를 구현하고, 에이전트가 대화의 맥락을 기억하게 만듭니다.
-   **[라이브 배포]** **`adk web`** 도구를 사용하여 완성된 에이전트 팀을 **라이브 웹 데모**로 배포하고 시연합니다.

---

## ⏰ 시간표 (총 6 세션, 15분 휴식)

| 세션 | 시간 | 내용 |
| :--- | :--- | :--- |
| **Session 1** | **09:30 – 10:20** (50분) | 설정 및 첫 번째 에이전트 정의 |
| 휴식 | 10:20 – 10:35 (15분) | |
| **Session 2** | **10:35 – 11:25** (50분) | 첫 번째 에이전트 실행하기 |
| 휴식 | 11:25 – 11:40 (15분) | |
| **Session 3** | **11:40 – 12:30** (50분) | [선택] LiteLLM을 이용한 멀티 모델 활용 |
| **점심 식사** | **12:30 – 13:30** (60분) | |
| **Session 4** | **13:30 – 14:20** (50분) | 에이전트 팀 빌딩 (위임) |
| 휴식 | 14:20 – 14:35 (15분) | |
| **Session 5** | **14:35 – 15:25** (50분) | 세션 스테이트로 메모리 추가하기 |
| 휴식 | 15:25 – 15:40 (15분) | |
| **Session 6** | **15:40 – 16:30** (50분) | **(신규)** `adk web`을 이용한 라이브 데모 배포 |

---
<br>

# 📚 세션별 상세 내용


## Session 1: 설정 및 첫 번째 에이전트 정의 (09:30 – 10:20)

### 🎯 학습 목표
-   과정 목표와 ADK 프레임워크를 이해합니다.
-   필수 라이브러리(ADK, LiteLLM)를 설치합니다.
-   여러 LLM 제공 업체의 API 키를 안전하게 구성합니다.
-   **Tool(도구)**(Python 함수)을 정의하고, **Docstring(설명문)**의 중요성을 이해합니다.
-   기본 **Agent(에이전트)**를 정의하고, `model`, `instruction`, `tools`를 설정합니다.

### 🧠 이론 및 개념
1.  **Overview:** ADK란 무엇인가? 왜 날씨 봇을 만드나? 6개 세션의 전체 계획을 리뷰합니다.
2.  **핵심 구성요소:** 사용자, 에이전트('두뇌'), Tool('손')의 관계를 설명합니다.
3.  **Tool Docstring:** LLM이 Tool의 사용법과 시기를 이해하기 위해 Docstring을 '읽는다'는 점을 강조합니다.

### 🛠️ 실습 (튜토리얼 단계 0 & 1 일부)
1.  **설정 (단계 0):** `!pip install google-adk litellm -q` 실행.
2.  **라이브러리 임포트 (단계 0):** 필요한 모든 라이브러리를 임포트합니다.
3.  **API 키 설정 (단계 0):** Gemini, OpenAI, Anthropic의 API 키를 환경 변수로 설정하도록 안내합니다.
4.  **Tool 정의 (단계 1):** `get_weather` 함수를 작성합니다. 이 함수의 Docstring을 상세히 분석합니다.
5.  **Agent 정의 (단계 1):** `weather_agent` (v1)를 생성합니다. `instruction` 프롬프트를 분석합니다.

***

## Session 2: 첫 번째 에이전트 실행하기 (10:35 – 11:25)

### 🎯 학습 목표
-   대화 관리를 위한 `SessionService`의 역할을 이해합니다.
-   에이전트의 실행 엔진인 `Runner`의 역할을 이해합니다.
-   `async`/`await`를 사용하여 에이전트와 비동기적으로 상호작용하는 방법을 배웁니다.
-   에이전트에게 쿼리를 보내고, Tool에 의해 생성된 응답을 성공적으로 수신합니다.

### 🧠 이론 및 개념
1.  **SessionService:** 대화 기록과 (나중에 배울) 메모리를 관리합니다. `InMemorySessionService`는 테스트용 임시 저장소입니다.
2.  **Runner:** 전체 흐름(사용자 입력 → LLM → Tool → LLM → 최종 응답)을 조율하는 엔진입니다.
3.  **Async & Events:** LLM/Tool 호출은 느린 작업(I/O)입니다. `asyncio`는 이를 효율적으로 실행합니다. `Runner`는 `Events`(예: "tool_requested", "final_response")를 반환하며, 우리는 이 이벤트를 관찰할 수 있습니다.

### 🛠️ 실습 (튜토리얼 단계 1 완료)
1.  **Runner 설정 (단계 1):** `InMemorySessionService`를 정의하고 `session`을 생성합니다. `Runner`를 정의합니다.
2.  **상호작용 함수 (단계 1):** `call_agent_async` 헬퍼 함수를 생성합니다. 왜 `is_final_response()`를 찾기 위해 이벤트를 반복하는지 설명합니다.
3.  **대화 실행 (단계 1):** `run_conversation` 블록을 실행합니다.
4.  **출력 분석:** 로그를 추적합니다: 사용자 쿼리 → `--- Tool: get_weather called... ---` → 에이전트 응답. "Paris" 오류 케이스를 테스트하고 에이전트가 지시대로 처리하는지 확인합니다.

***

## Session 3: [선택] LiteLLM을 이용한 멀티 모델 활용 (11:40 – 12:30)

### 🎯 학습 목표
-   작업에 따라 다른 LLM을 사용하는 것의 이점을 이해합니다.
-   ADK가 **LiteLLM**을 사용하여 모델 간의 차이점을 어떻게 추상화하는지 배웁니다.
-   GPT-4o와 Claude Sonnet을 사용하여 새 에이전트를 생성합니다.
-   *동일한 Tool*과 *동일한 로직*이 어떻게 다른 "두뇌"에 의해 구동될 수 있는지 관찰합니다.

### 🧠 이론 및 개념
1.  **왜 멀티 모델인가?** 성능, 비용, 기능 차이(튜토리얼 서문 참조)에 대해 논의합니다.
2.  **LiteLLM 래퍼:** `LiteLlm(model="provider/model_name")`가 ADK에게 LiteLLM 라이브러리를 통해 외부 모델을 호출하라고 지시하는 "마법"임을 설명합니다.

### 🛠️ 실습 (튜토리얼 단계 2)
1.  **GPT 에이전트 정의:** `LiteLlm(model=MODEL_GPT_4O)`를 사용하여 `weather_agent_gpt`를 생성합니다.
2.  **GPT Runner 설정:** GPT 테스트를 위해 *새롭고 분리된* `SessionService`와 `Runner`를 생성합니다.
3.  **GPT 에이전트 테스트:** 테스트 쿼리("What's the weather in Tokyo?")를 실행합니다.
4.  **Claude 에이전트 정의:** `LiteLlm(model=MODEL_CLAUDE_SONNET)`을 사용하여 `weather_agent_claude`에 대해 동일한 과정을 반복합니다.
5.  **Claude 에이전트 테스트:** 테스트 쿼리("Weather in London please.")를 실행합니다.
6.  **결과 비교:** 학생들에게 Gemini, GPT, Claude의 응답 *어조와 표현*을 비교해 보라고 요청합니다.

***

## Session 4: 에이전트 팀 빌딩 (위임) (13:30 – 14:20)

### 🎯 학습 목표
-   멀티 에이전트 시스템의 가치(모듈성, 전문화)를 이해합니다.
-   전문화된 **서브 에이전트**(`greeting_agent`, `farewell_agent`)를 정의합니다.
-   팀을 총괄하는 **루트 에이전트(Root Agent)**를 정의합니다.
-   서브 에이전트의 `description`(설명) 필드를 기반으로 **자동 위임(Automatic Delegation)**이 어떻게 작동하는지 이해합니다.

### 🧠 이론 및 개념
1.  **왜 에이전트 팀인가?** "모든 것을 하는" 단일 에이전트에서 "전문가 팀"으로 전환합니다.
2.  **루트 vs. 서브 에이전트:** 계층 구조를 설명합니다. 루트는 코디네이터, 서브는 전문가입니다.
3.  **자동 위임:** 루트 에이전트의 LLM이 서브 에이전트의 **`description`**을 읽고 작업을 위임한다는 것을 강조합니다. 좋은 `description`이 매우 중요합니다.

### 🛠️ 실습 (튜토리얼 단계 3)
1.  **새 Tool 정의:** `say_hello`와 `say_goodbye` 함수를 생성합니다.
2.  **서브 에이전트 정의:** `greeting_agent`와 `farewell_agent`를 생성합니다. 이들의 `description`과 `instruction` 필드를 면밀히 검토합니다.
3.  **루트 에이전트 정의:** `weather_agent_team` (v2)를 생성합니다.
    -   이 에이전트가 여전히 자신만의 Tool(`get_weather`)을 가지고 있음을 보여줍니다.
    -   새로운 `sub_agents=[...]` 파라미터를 강조합니다.
    -   이 에이전트의 `instruction`이 *언제* 위임해야 하는지 명시적으로 알려준다는 것을 분석합니다.
4.  **팀 테스트:** `run_team_conversation` 블록을 실행합니다.
5.  **로그 분석 (가장 중요):**
    -   "Hello there!" → `--- Tool: say_hello called ---`
    -   "Weather in New York?" → `--- Tool: get_weather called ---`
    -   "Thanks, bye!" → `--- Tool: say_goodbye called ---`
    -   결론: 위임이 성공적으로 작동함을 확인합니다!

***

## Session 5: 세션 스테이트로 메모리 추가하기 (14:35 – 15:25)

### 🎯 학습 목표
-   에이전트가 맥락 있는 대화를 위해 **메모리(Session State)**를 필요로 하는 이유를 이해합니다.
-   Tool이 `ToolContext`를 전달받아 상태(State)를 **읽는** 방법을 배웁니다.
-   Tool이 `tool_context.state`를 사용하여 상태에 **쓰는** 방법을 배웁니다.
-   에이전트의 `output_key`를 사용하여 에이전트의 최종 응답을 상태에 **자동 저장**하는 방법을 배웁니다.

### 🧠 이론 및 개념
1.  **세션 스테이트란?** 특정 사용자 세션에 연결된 영구적인 파이썬 딕셔너리(`session.state`)입니다.
2.  **`ToolContext`:** `get_weather_stateful` 같은 Tool이 세션의 상태에 접근할 수 있게 해주는 "다리"입니다.
3.  **`output_key`:** "내 최종 텍스트 응답이 무엇이든, `session.state['my_key']`에 저장해"라는 간단한 에이전트 설정입니다.

### 🛠️ 실습 (튜토리얼 단계 4)
1.  **상태 초기화:** *새로운* 세션(`session_service_stateful`)을 만들고, 생성 시 `initial_state`를 전달합니다.
2.  **상태 인식 Tool 정의:** `get_weather_stateful`을 생성합니다.
    -   새로운 `tool_context: ToolContext` 파라미터를 보여줍니다.
    -   `tool_context.state.get(...)` 라인(단위 읽기)을 보여줍니다.
    -   온도 변환 로직을 보여줍니다.
    -   `tool_context.state["last_city_checked_stateful"] = city` 라인(상태 쓰기)을 보여줍니다.
3.  **상태 인식 에이전트 정의:** `root_agent_stateful` (v4)를 생성합니다.
    -   새로운 `get_weather_stateful` Tool을 사용하는 것을 보여줍니다.
    -   새로운 `output_key="last_weather_report"` 파라미터를 강조합니다.
4.  **상태 흐름 테스트:** `run_stateful_conversation` 블록을 실행합니다.
5.  **흐름 분석:**
    -   턴 1 (London): Tool이 "Celsius"(초기 상태)를 읽음.
    -   수동 업데이트: 테스트를 위해 상태를 "Fahrenheit"로 *수동* 변경.
    -   턴 2 (New York): Tool이 "Fahrenheit"(새 상태)를 읽고 온도를 변환.
    -   최종 상태 검사: `final_session.state`를 확인하여 `user_preference_temperature_unit`이 "Fahrenheit"인지, `last_city_checked_stateful`이 "New York"인지, `last_weather_report`가 에이전트가 *마지막으로* 말한 내용인지 확인.

***

## Session 6: (신규) `adk web`을 이용한 라이브 데모 배포 (15:40 – 16:30)

### 🎯 학습 목표
-   '노트북 테스트 모드'와 '서버 실행 모드'의 차이점을 이해합니다.
-   여러 셀의 코드를 하나의 파이썬 스크립트(`main.py`)로 리팩토링합니다.
-   `adk web` 명령어를 사용하여 에이전트 챗봇 서버를 실행합니다.
-   **웹 UI 데모**에 접속하여 Session 5까지 만든 **메모리 기능이 있는 에이전트 팀**을 라이브로 시연합니다.

### 🧠 이론 및 개념
1.  **`adk web`이란?** `adk web <파일.py>`는 ADK가 자동으로 `Runner`와 `SessionService`를 관리하며, **웹 기반 챗봇 UI**를 생성해주는 강력한 배포 도구입니다.
2.  **코드 리팩토링:** 노트북의 `await call_agent_async(...)` 같은 수동 실행 코드는 더 이상 필요 없습니다. `adk web`은 에이전트 '정의'만 있으면 됩니다.

### 🛠️ 실습 (Workbench 터미널 & UI)
1.  **[코드 리팩토링]** JupyterLab 파일 탐색기에서 `main.py`라는 새 파일을 생성합니다.
2.  **[코드 복사]** Session 1~5에서 **'정의'**한 모든 코드를 `main.py`에 복사합니다.
    -   모든 `import` 문
    -   API 키 설정 (`os.environ[...]`)
    -   Tool 정의: `get_weather_stateful`, `say_hello`, `say_goodbye`
    -   Agent 정의: `greeting_agent`, `farewell_agent`, `root_agent_stateful` (v4)
3.  **[필수 코드 추가]** `main.py` 파일 **맨 아래**에 `adk web`이 루트 에이전트를 인식할 수 있도록 다음 코드를 추가합니다.
    ```python
    # main.py 맨 아래 추가
    #
    # root_agent_stateful 변수가 S5에서 정의한 최종 에이전트여야 함
    if __name__ == "__main__":
        from google.adk.tools.adk_tool import AdkTool
        
        # ADK가 이 파일을 실행할 때 'root_agent_stateful'을
        # 메인 에이전트로 사용하도록 등록합니다.
        AdkTool(agent=root_agent_stateful).run()
    ```
4.  **[서버 실행]** JupyterLab에서 `File > New > Terminal`을 열어 새 터미널을 시작합니다.
5.  터미널에서 다음 명령어를 실행하여 웹 서버를 시작합니다.
    ```bash
    adk web main.py --port=8080
    ```
6.  **[라이브 데모]** 서버가 실행되면, Vertex AI Workbench 우측 상단의 **'미리보기(Preview)'** 버튼을 클릭하고 **'포트 8080에서 미리보기'**를 선택합니다.
7.  **[최종 테스트]** 새 브라우저 탭에 **ADK가 생성한 챗봇 UI**가 나타납니다.
8.  학생들은 이 웹 UI에서 "Hello", "날씨 알려줘", "Fahrenheit로 바꿔줘"(*이건 S5에서 Tool로 구현해야 함*), "잘 가" 등을 입력하며 **메모리와 위임 기능이 모두 작동하는 라이브 서비스**를 직접 체험하며 과정을 마무리합니다.
