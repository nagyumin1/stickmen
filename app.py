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
    spawn_btn = st.button("💥 새로운 스틱맨 소환 (시각 효과)")
with col3:
    st.slider("스틱맨 분노 게이지 (속도 조절)", 1, 10, 5)

st.text_area("방명록 낙서장", "여기에 글을 쓰면 스틱맨들이 밟고 지나갈지도 모릅니다...")

# 3. HTML & JavaScript 코드 (따옴표 에러 해결 버전)
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
window.parent.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

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

        let leftHandX = this.x - this.size * 1.5 * Math.sin(this.angle);
        let leftHandY = bodyY + this.size * Math.cos(this.angle) + 5;
        let rightHandX = this.x + this.size * 1.5 * Math.sin(this.angle);
        let rightHandY = bodyY - this.size * Math.cos(this.angle) + 5;

        ctx.beginPath();
        ctx.moveTo(this.x, bodyY + 5);
        ctx.lineTo(leftHandX, leftHandY);
        ctx.moveTo(this.x, bodyY + 5);
        ctx.lineTo(rightHandX, rightHandY);
        ctx.stroke();

        let leftFootX = this.x - this.size * 1.5 * Math.cos(this.angle);
        let leftFootY = pelvisY + this.size * 1.5 * Math.abs(Math.sin(this.angle));
        let rightFootX = this.x + this.size * 1.5 * Math.cos(this.angle);
        let rightFootY = pelvisY + this.size * 1.5 * Math.abs(Math.cos(this.angle));

        ctx.beginPath();
        ctx.moveTo(this.x, pelvisY);
        ctx.lineTo(leftFootX, leftFootY);
        ctx.moveTo(this.x, pelvisY);
        ctx.lineTo(rightFootX, rightFootY);
        ctx.stroke();
    }
}

const stickmen = [
    new Stickman(200, 300, '#FF3333'),
    new Stickman(400, 200, '#33FF33'),
    new Stickman(600, 400, '#3333FF'),
    new Stickman(800, 500, '#FFFF33')
];

let drawings = [];

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    stickmen.forEach(s => {
        if (Math.random() < 0.05) {
            drawings.push({x: s.x, y: s.y + 35, color: s.color, alpha: 1.0});
        }
    });

    drawings.forEach((d, index) => {
        ctx.strokeStyle = d.color;
        ctx.globalAlpha = d.alpha;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(d.x, d.y, 2, 0, Math.PI * 2);
        ctx.stroke();
        d.alpha -= 0.005;
        if (d.alpha <= 0) drawings.splice(index, 1);
    });
    ctx.globalAlpha = 1.0;

    stickmen.forEach(s => {
        s.update();
        s.draw();
    });

    requestAnimationFrame(animate);
}

animate();
</script>
"""

# HTML 컴포넌트 호출
components.html(stickman_html, height=0)

# 4. 화면 전체를 덮도록 커스텀 CSS 주입
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
