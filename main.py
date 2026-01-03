import os
import requests
import sqlite3
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

load_dotenv()

# DB 초기화
def init_db():
    conn = sqlite3.connect('mlb_dugout.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            hr INTEGER,
            rbi INTEGER,
            avg TEXT,
            ops TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@tool("mlb_player_stats_tool")
def mlb_player_stats_tool(player_name: str) -> str:
    """MLB 선수의 성적을 조회하고 DB에 기록합니다."""
    try:
        search_url = f"https://statsapi.mlb.com/api/v1/people/search?names={player_name}"
        search_res = requests.get(search_url).json()
        if not search_res.get('people'): return f"{player_name} 선수를 찾을 수 없습니다."
        
        player_id = search_res['people'][0]['id']
        stats_url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&group=hitting"
        stats_res = requests.get(stats_url).json()
        
        if 'stats' in stats_res and stats_res['stats']:
            s = stats_res['stats'][0]['splits'][0]['stat']
            hr, rbi, avg, ops = s.get('homeRuns', 0), s.get('rbi', 0), s.get('avg', '.000'), s.get('ops', '.000')
            
            conn = sqlite3.connect('mlb_dugout.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO player_stats (player_name, hr, rbi, avg, ops) VALUES (?, ?, ?, ?, ?)', 
                           (player_name, hr, rbi, avg, ops))
            conn.commit()
            conn.close()
            return f"[{player_name} 최신 성적] 홈런: {hr}, 타점: {rbi}, 타율: {avg}, OPS: {ops}"
        return "데이터를 찾을 수 없습니다."
    except Exception as e:
        return f"오류: {str(e)}"

# LLM 설정
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    safety_settings={HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE}
)

data_scouter = Agent(
    role='MLB 데이터 전문가',
    goal='최신 뉴스 및 선수 성적을 수집하고 수치 기반의 분석을 수행합니다.',
    backstory='당신은 복잡한 세이버메트릭스 데이터를 알기 쉽게 요약하는 전문가입니다.',
    tools=[SerperDevTool(), mlb_player_stats_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role='스포츠 전문 기자',
    goal='분석된 데이터를 바탕으로 독창적인 한국어 리포트를 작성합니다.',
    backstory='당신은 야구 팬들의 흥미를 자극하는 몰입감 있는 글을 씁니다.',
    llm=llm,
    verbose=True
)

def run_mlb_crew(question):
    chat_task = Task(
        description=f"사용자 질문: {question}. 데이터를 수집하고 인사이트가 담긴 한국어 답변을 작성하세요.",
        expected_output="사용자 질문에 대한 전문적인 답변 (한국어)",
        agent=data_scouter
    )
    crew = Crew(agents=[data_scouter, writer], tasks=[chat_task], process=Process.sequential)
    return crew.kickoff()
