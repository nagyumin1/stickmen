import streamlit as st
import streamlit.components.v1 as components
import os

# 1. 스트림릿 페이지 설정
st.set_page_config(
    page_title="Animation vs. Streamlit v2.1",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ Animation vs. Streamlit (Ver 2.1)")
st.caption("차분해진 스틱맨들을 마우스로 꾹 눌러서 원하는 곳으로 옮겨보세요!")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리")
with col2:
    st.button("💥 새로운 스틱맨 소환 (준비 중)")
with col3:
    st.slider("스틱맨 안정 수치", 1, 10, 9)

st.text_area("방명록 낙서장", "마우스로 졸라맨을 잡아서 여기다 던져 놓을 수 있습니다.")

# 2. index.html 파일 안전하게 읽어오기
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=0)
else:
    st.error("index.html 파일을 찾을 수 없습니다. main.py와 같은 폴더에 생성해 주세요!")

# 3. 마우스 클릭 관통 스타일 설정
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
        pointer-events: none;
    }
    .stApp * {
        pointer-events: auto;
    }
    </style>
""", unsafe_allow_html=True)
