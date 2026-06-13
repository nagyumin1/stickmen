import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(
    page_title="Animation vs. Streamlit",
    page_icon="✏️",
    layout="wide"
)

# 2. 상단 타이틀 및 설명
st.title("✏️ Animation vs. Streamlit (Ver 2.0)")
st.caption("중력, 자연스러운 보행 모션, 마우스 클릭 상호작용 및 지들끼리 몸싸움하는 스틱맨들입니다!")

# UI 컴포넌트 배치
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 액티브 스틱맨", value="4 마리", delta="▲ 1")
with col2:
    st.button("💥 새로운 스틱맨 소환 (시각 효과)")
with col3:
    st.slider("스틱맨 분노 게이지 (속도 조절)", 1, 10, 5)

st.text_area("방명록 낙서장", "여기에 글을 쓰면 스틱맨들이 밟고 지나갈지도 모릅니다...")

# 3. 텍스트 깨짐 방지를 위해 자바스크립트 코드를 안전한 작은 조각으로 조립
code_pieces = [
    '<div id="canvas-container" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:auto;z-index:9999;">',
    '<canvas id="stickmanCanvas"></canvas>',
    '</div>',
    '<script>',
    'const canvas=document.getElementById("stickmanCanvas");const ctx=canvas.getContext("2d");',
    'function resizeCanvas(){canvas.width=window.innerWidth;canvas.height=window.innerHeight;}',
    'window.addEventListener("resize",resizeCanvas);resizeCanvas();',
    'const GRAVITY=0.4;const FRICTION=0.98;',
    'let mouse={x:window.innerWidth/2,y:window.innerHeight/2};',
    'window.parent.addEventListener("mousemove",(e)=>{mouse.x=e.clientX;mouse.y=e.clientY;});',
    'window.parent.addEventListener("mousedown",(e)=>{',
    'stickmen.forEach(s=>{',
    'let dx=e.clientX-s.x;let dy=e.clientY-s.y;let dist=Math.sqrt(dx*dx+dy*dy);',
    'if(dist<80){s.vx=(dx===0?(Math.random()-0.5)*10:-dx/dist*15);s.vy=-12;s.state="surprised";s.stateTimer=45;}',
    '});',
    '});',
    'class Stickman{',
    'constructor(x,y,color){',
    'this.x=x;this.y=y;this.color=color;this.size=12;this.vx=(Math.random()-0.5)*5;this.vy=0;',
    'this.walkCycle=Math.random()*Math.PI*2;this.state="walk";this.stateTimer=0;this.groundY=canvas.height-30;',
    '}',
    'update(){',
    'this.groundY=canvas.height-30;',
    'if(this.stateTimer>0){this.stateTimer--;if(this.stateTimer===0)this.state="walk";}',
    'if(this.state==="walk"){',
    'if(Math.random()<0.02)this.vx+=(Math.random()-0.5)*4;',
    'if(Math.random()<0.005){let dx=mouse.x-this.x;this.vx+=Math.sign(dx)*2;}',
    '}',
    'this.vy+=GRAVITY;this.vx*=FRICTION;this.x+=this.vx;this.y+=this.vy;',
    'if(this.y>=this.groundY){',
    'this.y=this.groundY;this.vy=0;',
    'if(Math.abs(this.vx)>0.2)this.walkCycle+=Math.abs(this.vx)*0.15;',
    'if(this.state==="walk"&&Math.random()<0.01)this.vy=-Math.random()*8-4;',
    '}',
    'if(this.x<30){this.x=30;this.vx*=-0.5;}if(this.x>canvas.width-30){this.x=canvas.width-30;this.vx*=-0.5;}',
    '}',
    'draw(){',
    'ctx.strokeStyle=this.color;ctx.lineWidth=4;ctx.lineCap="round";ctx.fillStyle=this.color;',
    'ctx.beginPath();ctx.arc(this.x,this.y-this.size,this.size,0,Math.PI*2);ctx.stroke();',
    'if(this.state==="surprised"){ctx.font="bold 16px sans-serif";ctx.fillText("!!",this.x-8,this.y-this.size*2.5);}',
    'else if(this.state==="annoyed"){ctx.font="bold 16px sans-serif";ctx.fillText("?!",this.x-8,this.y-this.size*2.5);}',
    'let torsoTop=this.y;let torsoBottom=this.y+this.size*1.8;',
    'ctx.beginPath();ctx.moveTo(this.x,torsoTop);ctx.lineTo(this.x,torsoBottom);ctx.stroke();',
    'let leftLegAngle,rightLegAngle,leftArmAngle,rightArmAngle;',
    'if(this.y<this.groundY){leftLegAngle=0.4;rightLegAngle=-0.4;leftArmAngle=-0.8;rightArmAngle=0.8;}',
    'else if(this.state==="surprised"){leftLegAngle=-0.2;rightLegAngle=0.2;leftArmAngle=-2.2;rightArmAngle=2.2;}',
    'else{let swing=Math.sin(this.walkCycle)*0.6;leftLegAngle=swing;rightLegAngle=-swing;leftArmAngle=-swing*0.5;rightArmAngle=swing*0.5;}',
    'let legLength=this.size*1.8;',
    'ctx.beginPath();ctx.moveTo(this.x,torsoBottom);ctx.lineTo(this.x+Math.sin(leftLegAngle)*legLength,torsoBottom+Math.cos(leftLegAngle)*legLength);',
    'ctx.moveTo(this.x,torsoBottom);ctx.lineTo(this.x+Math.sin(rightLegAngle)*legLength,torsoBottom+Math.cos(rightLegAngle)*legLength);ctx.stroke();',
    'let armLength=this.size*1.5;let armY=torsoTop+this.size*0.5;',
    '
