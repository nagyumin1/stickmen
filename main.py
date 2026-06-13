import streamlit as st
import streamlit.components.v1 as components
import os

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit",
    page_icon="✏️",
    layout="wide"
)

# 2. 상단 UI 배치
st.title("✏️ Animation vs. Streamlit")
st.caption("중력, 자연스러운 보행 모션, 마우스 상호작용이 완성된 스틱맨들입니다!")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 1")
with col2:
    st.button("💥 새로운 스틱맨 소환 (시각 효과)")
with col3:
    st.slider("스틱맨 분노 게이지 (속도 조절)", 1, 10, 5)

st.text_area("방명록 낙서장", "여기에 글을 쓰면 스틱맨들이 밟고 지나갈지도 모릅니다...")

# 3. 🔥 에러 원천 차단: 외부 index.html 파일 읽어오기
# 파이썬 문자열 파서를 거치지 않고 파일 시스템에서 직접 읽어 주입하므로 문법 에러가 불가능합니다.
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=0)
else:
    st.error("index.html 파일을 찾을 수 없습니다. main.py와 같은 경로에 생성해 주세요!")

# 4. 레이어 제어 스타일 주입
st.markdown("""
    <style>
    iframe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw !important;
        height: 100vh !important;
        border: none;
        pointer-events: auto;
        z-index: 99999;
    }
    .stApp {
        position: relative;
        z-index: 1;
    }
    </style>
""", unsafe_allow_html=True)
