import os
import requests  # mlbstatsapi 대신 표준 requests 사용
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai.tools import tool

# 1. 환경 변수 로드 및 폴더 생성
load_dotenv()

if not os.path.exists('reports'):
    os.makedirs('reports')

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
report_filename = f"reports/{timestamp}.md"

# 2. 커스텀 도구 정의 (코드 상단으로 올리기)
@tool("mlb_player_stats_tool")
def mlb_player_stats_tool(player_name: str) -> str:
    """MLB 선수의 이름을 영어로 입력하면 해당 선수의 현재 시즌 주요 성적을 반환합니다.
    예: 'Shohei Ohtani', 'Ha-Seong Kim'
    """
    try:
        # 1. 선수 ID 검색
        search_url = f"https://statsapi.mlb.com/api/v1/people/search?names={player_name}"
        search_res = requests.get(search_url).json()
        
        if not search_res.get('people'):
            return f"{player_name} 선수를 찾을 수 없습니다."
        
        player_id = search_res['people'][0]['id']
        
        # 2. 시즌 성적 조회
        stats_url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&group=hitting"
        stats_res = requests.get(stats_url).json()
        
        if 'stats' in stats_res and stats_res['stats']:
            s = stats_res['stats'][0]['splits'][0]['stat']
            hr = s.get('homeRuns', 0)
            rbi = s.get('rbi', 0)
            avg = s.get('avg', '.000')
            ops = s.get('ops', '.000')
            return f"[{player_name} 성적] 홈런: {hr}, 타점: {rbi}, 타율: {avg}, OPS: {ops}"
        
        return f"{player_name}의 성적 데이터가 없습니다."
    except Exception as e:
        return f"데이터 조회 중 오류 발생: {str(e)}"

# 3. Gemini 설정
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 4. 에이전트 정의 (data_scouter로 수정)
data_scouter = Agent(
    role='MLB 데이터 및 뉴스 스카우터',
    goal='오늘의 주요 뉴스뿐만 아니라 핵심 선수들의 실제 경기 기록을 수집합니다.',
    backstory='당신은 숫자를 신뢰하는 세이버메트릭스 전문가이자 스카우트입니다.',
    tools=[SerperDevTool(), mlb_player_stats_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role='스포츠 전문 칼럼니스트',
    goal='수집된 데이터를 바탕으로 한국어 브리핑 리포트를 작성합니다.',
    backstory='당신은 복잡한 야구 용어를 쉽게 풀이하는 전문 기자입니다.',
    llm=llm,
    verbose=True
)

# 5. 작업 정의 (news_scouter 대신 data_scouter 사용)
search_task = Task(
    description='오늘의 MLB 주요 뉴스 3가지를 찾고, "Shohei Ohtani"의 현재 시즌 성적을 도구로 가져오세요.',
    expected_output='MLB 뉴스 요약과 오타니의 성적이 포함된 정보',
    agent=data_scouter
)

write_task = Task(
    description='수집된 정보를 바탕으로 블로그 포스팅 스타일의 한국어 리포트를 작성하세요.',
    expected_output='마크다운 형식의 리포트',
    agent=writer,
    output_file=report_filename
)

# 6. 크루 실행 (data_scouter 확인!)
mlb_dugout_crew = Crew(
    agents=[data_scouter, writer],
    tasks=[search_task, write_task],
    process=Process.sequential
)

print(f"## MLB Dugout AI 가동 (파일: {report_filename}) ##")
mlb_dugout_crew.kickoff()
