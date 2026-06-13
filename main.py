import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit (Alan Becker Tribute)",
    page_icon="✏️",
    layout="wide"
)

# 2. 상단 타이틀 및 설명 (Alan Becker 감성 테마)
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

# 3. 핵심: 주신 원본 HTML + JS 코드를 줄바꿈 버그 없이 안전하게 주입
stickman_html = """
<div id="canvas-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999;">
    <canvas id="stickmanCanvas"></canvas>
</div>

<script>
const canvas = document.getElementById('stickmanCanvas');
const ctx = canvas.getContext('2d');

// 화면 크기 맞추기
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// 마우스 위치 추적 (Alan Becker 작품 특유의 '마우스 커서 공격'용)
let mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
window.parent.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

// 스틱맨 클래스 정의
class Stickman {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = 12; // 머리 크기 기준
        this.vx = (Math.random() - 0.5) * 4;
        this.vy = (Math.random() - 0.5) * 4;
        this.angle = 0;
        this.state = 'walk'; // walk, jump, attack
        this.targetX = mouse.x;
        this.targetY = mouse.y;
    }

    update() {
        // 주기적으로 마우스 커서나 무작위 위치를 향해 이동
        if (Math.random() < 0.02) {
            this.targetX = mouse.x + (Math.random() - 0.5) * 200;
            this.targetY = mouse.y + (Math.random() - 0.5) * 200;
        }

        // 가속도 계산 (마우스 추적 흉내)
        let dx = this.targetX - this.x;
        let dy = this.targetY - this.y;
        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > 50) {
            this.vx += (dx / dist) * 0.2;
            this.vy += (dy / dist) * 0.2;
        }

        // 속도 제한 및 마찰력
        this.vx *= 0.98;
        this.vy *= 0.98;

        this.x += this.vx;
        this.y += this.vy;

        // 벽 리바운드 제어 (화면 밖 탈출 방지)
        if (this.x < 50 || this.x > canvas.width - 50) this.vx *= -1;
        if (this.y < 50 || this.y > canvas.height - 50) this.vy *= -1;

        this.angle += Math.sqrt(this.vx*this.vx + this.vy*this.vy) * 0.05;
    }

    draw() {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';

        // 1. 머리 그리기
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.stroke();

        // 2. 몸통 그리기
        let bodyY = this.y + this.size;
        let pelvisY = bodyY + this.size * 2;
        ctx.beginPath();
        ctx.moveTo(this.x, bodyY);
        ctx.lineTo(this.x, pelvisY);
        ctx.stroke();

        // 3. 팔 그리기 (달리는 모션 반영)
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

        // 4. 다리 그리기 (달리는 모션 반영)
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

// 오리지널 색상 스틱맨 무리 생성 (The Chosen One, Second Coming, Green, Blue 등 컨셉)
const stickmen = [
    new Stickman(200, 300, '#FF3333'), // 빨강 (The Second Coming)
    new Stickman(400, 200, '#33FF33'), // 초록 (Green)
    new Stickman(600, 400, '#3333FF'), // 파랑 (Blue)
    new Stickman(800, 500, '#FFFF33')  // 노랑 (Yellow)
];

// 간단한 배경 낙서 저장 배열
let drawings = [];

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 가끔 스틱맨이 지나간 자리에 낙서 흔적 남기기
    stickmen.forEach(s => {
        if (Math.random() < 0.05) {
            drawings.push({x: s.x, y: s.y + 35, color: s.color, alpha: 1.0});
        }
    });

    // 낙서 그리기 및 수명 깎기
    drawings.forEach((d, index) => {
        ctx.strokeStyle = d.color;
        ctx.globalAlpha = d.alpha;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(d.x, d.y, 2, 0, Math.PI * 2);
        ctx.stroke();
        d.alpha -= 0.005; // 서서히 사라짐
        if (d.alpha <= 0) drawings.splice(index, 1);
    });
    ctx.globalAlpha = 1.0; // 투명도 초기화

    // 스틱맨 업데이트 및 렌더링
    stickmen.forEach(s => {
        s.update();
        s.draw();
    });

    requestAnimationFrame(animate);
}

animate();
</script>
"""

# 서버가 문자열을 깨뜨리지 못하도록 base64 인코딩 주입
b64_html = base64.b64encode(stickman_html.encode('utf-8')).decode('utf-8')
components.iframe(src=f"data:text/html;base64,{b64_html}", height=0)

# 4. 스타일 우회 주입 (오타 수정 완료)
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
