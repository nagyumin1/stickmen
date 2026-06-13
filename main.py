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

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 1")
with col2:
    st.button("💥 새로운 스틱맨 소환 (시각 효과)")
with col3:
    st.slider("스틱맨 분노 게이지 (속도 조절)", 1, 10, 5)

st.text_area("방명록 낙서장", "여기에 글을 쓰면 스틱맨들이 밟고 지나갈지도 모릅니다...")

# 3. 핵심: 주석을 100% 제거하여 찢어짐/한줄합치기 버그를 차단한 HTML
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
} catch(err) {}

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
        }

        this.vx *= 0.98;
        this.vy *= 0.98;
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 50 || this.x > canvas.width - 50) this.vx *= -1;
        if (this.y < 50 || this.y > canvas.height - 50) this.vy *= -1;

        this.angle += Math.sqrt(this.vx*this.vx + this.vy*this.vy) * 0.05;
    }

    draw() {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';

        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.stroke();

        let bodyY = this.y + this.size;
        let pelvisY = bodyY + this.size * 2;
        ctx.beginPath();
        ctx.moveTo(this.x, bodyY);
        ctx.lineTo(this.x, pelvisY);
        ctx.stroke();

        let
