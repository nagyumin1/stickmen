]import streamlit as st
import streamlit.components.v1 as components
import os

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit (Alan Becker Tribute)",
    page_icon="✏️",
    layout="wide"
)

# 2. 상단 UI 배치
st.title("✏️ Animation vs. Streamlit")
st.caption("Alan Becker의 작품 세계처럼, 스틱맨들이 스트림릿 앱 내부를 자유롭게 난입합니다!")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 1")
with col2:
    st.button("💥 새로운 스틱맨 소환 (시각 효과)")
with col3:
    st.slider("스틱맨 분노 게이지 (속도 조절)", 1, 10, 5)

st.text_area("방명록 낙서장", "여기에 글을 쓰면 스틱맨들이 밟고 지나갈지도 모릅니다...")

# 3. 핵심: 외부 html 파일을 안전하게 읽어와 컴포넌트로 실행 (안 터짐 보장)
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    # 브라우저 활성화를 위해 충분한 높이 인젝션
    components.html(html_content, height=600)
else:
    st.error("index.html 파일을 찾을 수 없습니다. main.py와 같은 위치에 생성해 주세요!")

# 4. 스타일 우회 주입 (전체 화면 투명 레이어로 배치)
st.markdown("""
    <style>
    iframe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw !important;
        height: 100vh !important;
        border: none;
        pointer-events: none;
        z-index: 99999;
    }
    </style>
""", unsafe_allow_html=True)
