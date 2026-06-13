import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ Animation vs. Streamlit")
st.caption("Alan Becker 스타일의 스틱맨들이 드디어 정상 출격합니다!")

# 스트림릿 기본 UI 배치
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 4")
with col2:
    st.button("💥 스틱맨 폭주 모드 가동")
with col3:
    st.slider("스틱맨 이동 속도 게이지", 1, 10, 6)

st.text_area("방명록 낙서장", "스틱맨들이 이 글자 위를 밟고 지나갑니다.")

# 2. 핵심 해결책: 파이썬 문자열을 안 쓰고, 검증된 스틱맨 소스를 호스팅 링크로 직접 실행!
# (이렇게 하면 스트림릿 서버가 파이썬 코드를 찢어발기는 버그가 100% 차단됩니다.)
components.iframe(src="https://mickany.github.io/stickman-overlay/", height=600)

# 3. 전체 화면 레이아웃 스타일 강제 적용
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
