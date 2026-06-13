import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ Animation vs. Streamlit")
st.caption("Alan Becker 스타일의 스틱맨들이 대시보드 위를 날아다닙니다!")

# 스트림릿 기본 UI 배치
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 4")
with col2:
    st.button("💥 스틱맨 폭주 모드 가동")
with col3:
    st.slider("스틱맨 이동 속도 게이지", 1, 10, 6)

st.text_area("방명록 낙서장", "스틱맨들이 이 글자 위를 밟고 지나갑니다.")

# 2. 버그 차단 핵심: 원본 소스코드를 깨지지 않는 안전한 Base64 문자열로 사전 변환
# (서버 배포 시 문자열 분실 및 줄바꿈 깨짐 현상을 원천 봉쇄합니다)
raw_code = """
<div id="canvas-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999;">
    <canvas id="stickmanCanvas"></canvas>
</div>
<script>
const canvas = document.getElementById("stickmanCanvas");
const ctx = canvas.getContext("2d");
function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
window.addEventListener("resize", resizeCanvas);
resizeCanvas();
let mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
window.addEventListener("mousemove", (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
try { window.parent.addEventListener("mousemove", (e) => { mouse.x = e.clientX; mouse.y = e.clientY; }); } catch(err) {}
class Stickman {
    constructor(x, y, color) {
        this.x = x; this.y = y; this.color = color; this.size = 12;
        this.vx = (Math.random() - 0.5) * 5; this.vy = (Math.random() - 0.5) * 5;
        this.angle = 0; this.targetX = mouse.x; this.targetY = mouse.y;
    }
    update() {
        if (Math.random() < 0.03) {
            this.targetX = mouse.x + (Math.random() - 0.5) * 300;
            this.targetY = mouse.y + (Math.random() - 0.5) * 300;
        }
        let dx = this.targetX - this.x; let dy = this.targetY - this.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist >
