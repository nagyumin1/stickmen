import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ Animation vs. Streamlit")
st.caption("그 어떤 인코딩 가위질도 이겨내고 스틱맨들이 드디어 정상 출격합니다!")

# 스트림릿 대시보드 UI 배치
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 4")
with col2:
    st.button("💥 스틱맨 폭주 모드 가동")
with col3:
    st.slider("스틱맨 이동 속도 게이지", 1, 10, 6)

st.text_area("방명록 낙서장", "스틱맨들이 이 글자 위를 밟고 지나갑니다.")

# 2. 해결책: 가위질할 틈을 주지 않도록 모든 줄바꿈과 공백을 박멸한 1줄짜리 크린 HTML
clean_html = '<div id="canvas-container" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;"><canvas id="stickmanCanvas"></canvas></div><script>const canvas=document.getElementById("stickmanCanvas");const ctx=canvas.getContext("2d");function resizeCanvas(){canvas.width=window.innerWidth;canvas.height=window.innerHeight}window.addEventListener("resize",resizeCanvas);resizeCanvas();let mouse={x:window.innerWidth/2,y:window.innerHeight/2};window.addEventListener("mousemove",(e)=>{mouse.x=e.clientX;mouse.y=e.clientY});try{window.parent.addEventListener("mousemove",(e)=>{mouse.x=e.clientX;mouse.y=e.clientY})}catch(err){}class Stickman{constructor(x,y,color){this.x=x;this.y=y;this.color=color;this.size=12;this.vx=(Math.random()-0.5)*5;this.vy=(Math.random()-0.5)*5;this.angle=0;this.targetX=mouse.x;this.targetY=mouse.y}update(){if(Math.random()<0.03){this.targetX=mouse.x+(Math.random()-0.5)*300;this.targetY=mouse.y+(Math.random()-0.5)*300}let dx=this.targetX-this.x;let dy=this.targetY-this.y;let dist=Math.sqrt(dx*dx+dy*dy);if(dist>30){this.vx+=(dx/dist)*0.25;this.vy+=(dy/dist)*0.25}this.vx*=0.97;this.vy*=0.97;this.x+=this.vx;this.y+=this.vy;if(this.x<40||this.x>canvas.width-40)this.vx*=-1;if(this.y<40||this.y>canvas.height-40)this.vy*=-1;this.angle+=Math.sqrt(this.vx*this.vx+this.vy*this.vy)*0.06}draw(){ctx.strokeStyle=this.color;ctx.lineWidth=3;ctx.lineCap="round";ctx.beginPath();ctx.arc(this.x,this.y,this.size,0,Math.PI*2);ctx.stroke();let bodyY=this.y+this.size;let pelvisY=bodyY+this.size*2;ctx.beginPath();ctx.moveTo(this.x,bodyY);ctx.lineTo(this.x,pelvisY);ctx.stroke();let lhX=this.x-this.size*1.5*Math.sin(this.angle);let lhY=bodyY+this.size*Math.cos(this.angle)+5;let rhX=this.x+this.size*1.5*Math.sin(this.angle);let rhY=bodyY-this.size*Math.cos(this.angle)+5;ctx.beginPath();ctx.moveTo(this.x,bodyY+5);ctx.lineTo(lhX,lhY);ctx.moveTo(this.x,bodyY+5);ctx.lineTo(rhX,rhY);ctx.stroke();let lfX=this.x-this.size*1.5*Math.cos(this.angle);let lfY=pelvisY+this.size*1.5*Math.abs(Math.sin(this.angle));let rfX=this.x+this.size*1.5*Math.cos(this.angle);let rfY=pelvisY+this.size*1.5*Math.abs(Math.cos(this.angle));ctx.beginPath();ctx.moveTo(this.x,pelvisY);ctx.lineTo(lfX,lfY);ctx.moveTo(this.x,pelvisY);ctx.lineTo(rfX,rfY);ctx.stroke()}}const stickmen=[new Stickman(200,300,"#FF3333"),new Stickman(400,200,"#33FF33"),new Stickman(600,400,"#3333FF"),new Stickman(800,500,"#FFFF33")];let drawings=[];function animate(){ctx.clearRect(0,0,canvas.width,canvas.height);stickmen.forEach(s=>{if(Math.random()<0.15){drawings.push({x:s.x,
