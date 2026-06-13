import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit (Alan Becker Tribute)",
    page_icon="✏️",
    layout="wide"
)

# 2. 상단 타이틀 및 설명
st.title("✏️ Animation vs. Streamlit (Ver 2.0)")
st.caption("중력, 자연스러운 보행 모션, 마우스 클릭 상호작용 및 지들끼리 몸싸움하는 스틱맨들입니다!")

# UI 상호작용용 간단한 스트림릿 컴포넌트 배치
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 1")
with col2:
    st.button("💥 새로운 스틱맨 소환 (시각 효과)")
with col3:
    st.slider("스틱맨 분노 게이지 (속도 조절)", 1, 10, 5)

st.text_area("방명록 낙서장", "여기에 글을 쓰면 스틱맨들이 밟고 지나갈지도 모릅니다...")

# 3. HTML & JavaScript 코드 (중력 + 보행 모션 + 상호작용 업그레이드)
stickman_html = """
<div id="canvas-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: auto; z-index: 9999;">
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

// 글로벌 물리 법칙 변수
const GRAVITY = 0.4;
const FRICTION = 0.98;

let mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
window.parent.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

// 마우스 클릭 이벤트 (스트림릿 부모 창 전체에서 감지)
window.parent.addEventListener('mousedown', (e) => {
    stickmen.forEach(s => {
        let dx = e.clientX - s.x;
        let dy = e.clientY - s.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        
        // 클릭 범위 안에 스틱맨이 있으면 깜짝 놀라며 튕겨나감
        if (dist < 80) {
            s.vx = (dx === 0 ? (Math.random() - 0.5) * 10 : -dx / dist * 15);
            s.vy = -12; // 위로 펄쩍 뜀
            s.state = 'surprised';
            s.stateTimer = 45; // 45프레임 동안 놀란 상태 유지
        }
    });
});

class Stickman {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = 12; // 머리 크기
        this.vx = (Math.random() - 0.5) * 5;
        this.vy = 0;
        this.walkCycle = Math.random() * Math.PI * 2;
        this.state = 'walk'; // walk, surprised, annoyed
        this.stateTimer = 0;
        this.groundY = canvas.height - 30;
    }

    update() {
        this.groundY = canvas.height - 30; // 실시간 화면 높이 반영

        // 타이머 감소 및 상태 복구
        if (this.stateTimer > 0) {
            this.stateTimer--;
            if (this.stateTimer === 0) this.state = 'walk';
        }

        // 일반 상태일 때 인공지능 움직임 (좌우 서성거리기)
        if (this.state === 'walk') {
            if (Math.random() < 0.02) {
                this.vx += (Math.random() - 0.5) * 4;
            }
            // 가끔 마우스 근처로 가고 싶어함
            if (Math.random() < 0.005) {
                let dx = mouse.x - this.x;
                this.vx += Math.sign(dx) * 2;
            }
        }

        // 물리 법칙 적용
        this.vy += GRAVITY;   // 중력 적용
        this.vx *= FRICTION;  // 마찰력 적용

        this.x += this.vx;
        this.y += this.vy;

        // 바닥 충돌 처리
        if (this.y >= this.groundY) {
            this.y = this.groundY;
            this.vy = 0;
            
            // 걷고 있을 때만 보행 사이클 누적 (움직이는 속도 비례)
            if (Math.abs(this.vx) > 0.2) {
                this.walkCycle += Math.abs(this.vx) * 0.15;
            }
            
            // 바닥에서 가끔 멍때리다가 점프
            if (this.state === 'walk' && Math.random() < 0.01) {
                this.vy = -Math.random() * 8 - 4;
            }
        }

        // 벽 충돌 처리
        if (this.x < 30) { this.x = 30; this.vx *= -0.5; }
        if (this.x > canvas.width - 30) { this.x = canvas.width - 30; this.vx *= -0.5; }
    }

    draw() {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 4;
        ctx.lineCap = 'round';
        ctx.fillStyle = this.color;

        // 1. 머리 그리기 (놀랐을 때는 표정 변화 유도용 타원이나 연출 가능)
        ctx.beginPath();
        ctx
