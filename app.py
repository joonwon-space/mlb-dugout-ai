import streamlit as st
import sqlite3
import pandas as pd
from main import run_mlb_crew

st.set_page_config(page_title="MLB Dugout AI", page_icon="⚾")
st.title("⚾ MLB Dugout AI")

# 대화 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바: 저장된 데이터 확인
with st.sidebar:
    st.header("📊 수집된 스탯")
    try:
        conn = sqlite3.connect('mlb_dugout.db')
        df = pd.read_sql_query("SELECT player_name, hr, rbi, created_at FROM player_stats ORDER BY created_at DESC LIMIT 10", conn)
        st.table(df)
        conn.close()
    except:
        st.write("아직 데이터가 없습니다.")

# 채팅 UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("질문을 입력하세요 (예: 오타니 현재 시즌 성적 분석해줘)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("에이전트가 분석 중..."):
            response = str(run_mlb_crew(prompt))
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})