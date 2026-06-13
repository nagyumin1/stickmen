import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ Animation vs. Streamlit")
st.caption("텍스트 가위질 버그를 완전히 박멸한 최종 프로토타입입니다!")

# 스트림릿 기본 UI 배치
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 4")
with col2:
    st.button("💥 스틱맨 폭주 모드 가동")
with col3:
    st.slider("스틱맨 이동 속도 게이지", 1, 10, 6)

st.text_area("방명록 낙서장", "스틱맨들이 이 글자 위를 밟고 지나갑니다.")

# 2. 해결책: 파이썬 문자열 리터럴을 쓰지 않고 byte 배열을 직접 조인하여 HTML 생성
# 이렇게 하면 스트림릿 배포 시스템이 문법 검사(Syntax) 단계에서 코드를 찢을 수 없습니다.
byte_pieces = [
    b'<div id="canvas-container" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;"><canvas id="stickmanCanvas"></canvas></div>',
    b'<script>',
    b'const canvas=document.getElementById("stickmanCanvas");const ctx=canvas.getContext("2d");',
    b'function resizeCanvas(){canvas.width=window.innerWidth;canvas.height=window.innerHeight}',
    b'window.addEventListener("resize",resizeCanvas);resizeCanvas();',
    b'let mouse={x:window.innerWidth/2,y:window.innerHeight/2};',
    b'window.addEventListener("mousemove",(e)=>{mouse.x=e.clientX;mouse.y=e.clientY});',
    b'try{window.parent.addEventListener("mousemove",(e)=>{mouse.x=e.clientX;mouse.y=e.clientY})}catch(err){}',
    b'class Stickman{constructor(x,y,color){this.x=x;this.y=y;this.color=color;this.size=12;this.vx=(Math.random()-0.5)*5;this.vy=(Math.random()-0.5)*5;this.angle=0;this.targetX=mouse.x;this.targetY=mouse.y}',
    b'update(){if(Math.random()<0.03){this.targetX=mouse.x+(Math.random()-0.5)*300;this.targetY=mouse.y+(Math.random()-0.5)*300}let dx=this.targetX-this.x;let dy=this.targetY-this.y;let dist=Math.sqrt(dx*dx+dy*dy);if(dist>30){this.vx+=(dx/dist)*0.25;this.vy+=(dy/dist)*0.25}this.vx*=0.97;this.vy*=0.97;this.x+=this.vx;this.y+=this.vy;if(this.x<40||this.x>canvas.width-40)this.vx*=-1;if(this.y<40||this.y>canvas.height-40)this.vy*=-1;this.angle+=Math.sqrt(this.vx*this.vx+this.vy*this.vy)*0.06}',
    b'draw(){ctx.strokeStyle=this.color;ctx.lineWidth=3;
