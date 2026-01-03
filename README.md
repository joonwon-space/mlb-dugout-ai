# ⚾ MLB-Dugout-AI 🤖

> **"MLB 실시간 데이터와 AI 에이전트를 결합하여, 나만의 지능형 야구 정보 플랫폼을 구축하는 프로젝트"**

이 프로젝트는 2026년 새해 목표인 '코딩 AI 에이전트 개발'의 첫 번째 결과물입니다. **CrewAI** 프레임워크와 **Claude 3.7 / Gemini 2.5** 모델을 활용하여, 메이저리그(MLB)의 방대한 데이터를 스스로 분석하고 사용자에게 가치 있는 통찰을 제공하는 'AI 덕아웃'을 만드는 것이 목표입니다.

## 🌟 프로젝트 비전
단순히 정보를 보여주는 웹사이트를 넘어, AI 에이전트가 데이터를 수집, 분석, 요약하고 웹 서비스 코드까지 스스로 개선해나가는 **자율형 서비스**를 지향합니다.

## 🗺️ 목표 달성 로드맵

### 1단계: 기초 다지기 (1~2월) - "에이전트 워밍업"
- [ ] 개발 환경 구축 (Python 3.10+, CrewAI, API 연결)
- [ ] **[Mission]** 오늘의 MLB 핵심 뉴스를 검색하여 한국어로 요약해주는 브리핑 에이전트 구현
- [ ] CrewAI의 `Agent`, `Task`, `Crew` 개념 완벽 숙달

### 2단계: 데이터 혈관 연결 (3~5월) - "데이터 스카우팅"
- [ ] `mlbstatsapi` 연동을 통한 실시간 경기 결과 및 선수 스탯 추출
- [ ] SQLite/SQLAlchemy를 활용한 장기 기록 보관 데이터베이스(DB) 설계
- [ ] **[Mission]** 에이전트가 직접 코드를 실행하여 데이터를 분석하고 그래프를 생성하는 기능 구현

### 3단계: 웹 서비스화 및 고도화 (6월~ ) - "메이저리그 데뷔"
- [ ] Streamlit 또는 React를 활용한 지능형 대시보드 구축
- [ ] 에이전트가 스스로 웹 UI 코드를 수정하고 배포 프로세스를 돕는 환경 구축
- [ ] **[Final Milestone]** 실시간 데이터와 AI 뉴스가 결합된 `mlb-dugout-ai` 서비스 런칭

## 🛠️ Tech Stack
- **Framework**: CrewAI, LangGraph
- **Intelligence**: Claude 3.7 Sonnet, Gemini 2.5 Pro
- **Language**: Python 3.10+
- **Data Source**: MLB Stats API, Google Search API (Serper)
- **Infrastructure**: Google Cloud Platform, GitHub Actions

---
*이 저장소는 AI 에이전트와 함께 성장하는 저의 도전 기록입니다.*
