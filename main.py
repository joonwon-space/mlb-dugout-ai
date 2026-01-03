import os
from datetime import datetime  # 날짜와 시간 처리를 위해 추가
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI # Gemini 로드

# 1. 환경 변수 로드
load_dotenv()

if not os.path.exists('reports'):
    os.makedirs('reports')

# 2. 현재 시간을 yyyymmdd-HHmmss 형식으로 추출
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
report_filename = f"reports/{timestamp}.md"

# 2. Gemini LLM 설정
# 모델명은 최신인 'gemini-2.0-pro-exp'(또는 현재 사용 가능한 최신 버전)를 입력하세요.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 3. 도구 설정
search_tool = SerperDevTool()

# 4. 에이전트 정의 (llm=llm 설정 추가)
news_scouter = Agent(
    role='MLB 뉴스 스카우터',
    goal='오늘의 메이저리그(MLB) 주요 소식과 경기 결과를 정확하게 찾아냅니다.',
    backstory='당신은 전 세계 야구 소식을 실시간으로 추적하는 전문 스카우트입니다.',
    tools=[search_tool],
    llm=llm, # <--- Gemini 할당
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='스포츠 전문 칼럼니스트',
    goal='수집된 뉴스를 바탕으로 팬들이 읽기 쉬운 한국어 브리핑 리포트를 작성합니다.',
    backstory='당신은 복잡한 야구 용어를 쉽게 풀이하는 10년 차 스포츠 전문 기자입니다.',
    llm=llm, # <--- Gemini 할당
    verbose=True,
    allow_delegation=False
)

# 5. 작업(Task) 정의
search_task = Task(
    description='오늘 날짜 기준 MLB의 가장 중요한 뉴스 3가지를 찾으세요. 오타니나 이정후 등 한국 선수 소식을 우선적으로 포함하세요.',
    expected_output='MLB 주요 뉴스 3가지의 핵심 내용 요약본',
    agent=news_scouter
)

write_task = Task(
    description='검색된 뉴스 요약본을 바탕으로 한국어 블로그 포스팅 스타일의 리포트를 작성하세요.',
    expected_output='마크다운(Markdown) 형식의 MLB 뉴스 한국어 브리핑 리포트',
    agent=writer,
    output_file=report_filename # <--- 이 줄을 추가하세요!
)

# 6. 크루(Crew) 결성 및 실행
mlb_dugout_crew = Crew(
    agents=[news_scouter, writer],
    tasks=[search_task, write_task],
    process=Process.sequential
)

print(f"## MLB Dugout AI 가동 시작 (파일 저장: {report_filename}) ##")
result = mlb_dugout_crew.kickoff()

print("\n\n################################")
print("## 오늘의 MLB 브리핑 결과 ##")
print("################################\n")
print(result)