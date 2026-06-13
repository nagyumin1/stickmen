import streamlit as st
import streamlit.components.v1 as components

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

# 3. 핵심: 스틱맨들을 자유롭게 움직이게 할 Canvas + JS 인젝션
# 스트림릿 화면 전체를 덮는 투명 canvas를 생성하여 애니메이션을 구현합니다.
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
            this.targetY = mouse
