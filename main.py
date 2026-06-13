import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit (Alan Becker Tribute)",
    page_icon="✏️",
    layout="wide"
)

# 2. 상단 타이틀 및 설명
st.title("✏️ Animation vs. Streamlit")
st.caption("Alan Becker의 작품 세계처럼, 스틱맨들이 스트림릿 앱 내부를 자유롭게 난입합니다!")

# UI 상호작용용 간단한 스트림릿 컴포넌트 배치
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 1")
with col2:
    st.button("💥 새로운 스틱맨 소환 (시각 효과)")
with col3:
    st.slider("스틱맨 분노 게이지 (속도 조절)", 1, 10, 5)

st.text_area("방명록 낙서장", "여기에 글을 쓰면 스틱맨들이 밟고 지나갈지도 모릅니다...")

# 3. 핵심: 안전하게 가독성을 높여 찢어짐 버그를 방지한 오리지널 JS 주입
# components.html 내부에서 실시간 렌더링되도록 높이를 지정하고 본체를 덮어씌웁니다.
stickman_html = """
<div id="canvas-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999;">
    <canvas id="stickmanCanvas"></canvas>
</div>

<script>
const canvas = document.getElementById('stickmanCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// 마우스 위치 추적 (iframe 보안 무시를 위해 window 자체 마우스 및 부모 마우스 동시 백업)
let mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };

window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

try {
    window.parent.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
} catch(e) {
    // CORS 방지용 안전 장치
}

class Stickman {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = 12;
        this.vx = (Math.random() - 0.5) * 4;
        this.vy = (Math.random() - 0.5) * 4;
        this.angle = 0;
        this.targetX = mouse.x;
        this.targetY = mouse.y;
    }

    update() {
        if (Math.random() < 0.02) {
            this.targetX = mouse.x + (Math.random() - 0.5) * 200;
            this.targetY = mouse.y + (Math.random() - 0.5) * 200;
        }

        let dx = this.targetX - this.x;
        let dy = this.targetY - this.y;
        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > 50) {
            this.vx += (dx / dist) * 0.2;
            this.vy += (dy / dist) * 0.2;
