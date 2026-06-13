import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. Streamlit Page Configuration
st.set_page_config(
    page_title="Stickman Simulation v2.1 (Calm & Controlled)",
    page_icon="✏️",
    layout="wide"
)

# 2. Page Title and Interface
st.title("✏️ Animation vs. Streamlit v2.1")
st.caption("A subdued simulation with controllable stickmen.")

# Minimal Streamlit UI
st.metric(label="Simulating Stickmen", value="4 Entities")
st.markdown("### Drag and Drop")
st.info("You can now click and drag the stickmen with your mouse.")

# 3. Enhanced Javascript with New Mechanics
raw_html = """
<div id="canvas-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: auto; z-index: 9999;">
    <canvas id="stickmanCanvas"></canvas>
</div>
<script>
const canvas = document.getElementById("stickmanCanvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

const GRAVITY = 0.35; // Slight reduction
const FRICTION = 0.96; // Slight increase to slow them down faster
const GROUND_OFFSET = 40; // Higher ground for readability

let mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2, isDown: false };
let draggedStickman = null;

window.parent.addEventListener("mousemove", (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

window.parent.addEventListener("mousedown", (e) => {
    mouse.isDown = true;
    
    // Check if mouse is over a stickman (prioritize heads for accuracy)
    stickmen.forEach(s => {
        let dxHead = e.clientX - s.x;
        let dyHead = e.clientY - (s.y - s.size * 2); // Body top
        let dist = Math.sqrt(dxHead * dxHead + dyHead * dyHead);
        if (dist < s.size * 3) { // generous selection area
            draggedStickman = s;
            s.vx = 0;
            s.vy = 0;
        }
    });
});

window.parent.addEventListener("mouseup", (e) => {
    mouse.isDown = false;
    draggedStickman = null;
});

class Stickman {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = 10;
        this.vx = 0;
        this.vy = 0;
        this.walkCycle = Math.random() * Math.PI * 2;
        this.stateTimer = 0;
        this.groundY = canvas.height - GROUND_OFFSET;
    }
    update() {
        this.groundY = canvas.height - GROUND_OFFSET;

        if (this.stateTimer > 0) {
            this.stateTimer--;
        }

        // Reduced random movement logic
        if (this === draggedStickman) {
            this.x = mouse.x;
            this.y = mouse.y;
            this.vx = 0;
            this.vy = 0;
        } else {
            if (this.y >= this.groundY) { // Only move randomly when on ground
                if (Math.random() < 0.003) { // 30% frequency reduction
                    this.vx += (Math.random() - 0.5) * 1.5; // halved power
                }
            }

            this.vy += GRAVITY;
            this.vx *= FRICTION;
            this.x += this.vx;
            this.y += this.vy;

            // Ground handling
            if (this.y >= this.groundY) {
                this.y = this.groundY;
                this.vy = 0;
                if (Math.abs(this.vx) > 0.1) {
                    this.walkCycle += Math.abs(this.vx) * 0.12;
                }
                
                // Significantly reduced random jump
                if (Math.random() < 0.002) { // 80% jump reduction
                    this.vy = -Math.random() * 5 - 2; // Reduced power
                }
            }
        }

        // Walls
        if (this.x < 40) { this.x = 40; this.vx *= -0.3; }
        if (this.x > canvas.width - 40) { this.x = canvas.width - 40; this.vx *= -0.3; }
        if (this.y < 50) { this.y = 50; this.vy *= -0.3; }
    }
    draw() {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.lineCap = "round";
        ctx.fillStyle = this.color;

        // Condition check for exclamation marks (only 20% of collisions)
        let showExclamation = false;
        if (this.stateTimer > 0) {
            stickmen.forEach(other => {
                if (this !== other) {
                    let dx = other.x - this.x;
                    let dy = other.y - this.y;
                    let dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 40) { // Collision radius
                        if (Math.random() < 0.20) { // 20% frequency
                            showExclamation = true;
                        }
                    }
                }
            });
        }

        if (showExclamation) {
            ctx.font = "bold 18px sans-serif";
            ctx.fillText("!!", this.x - 7, this.y - this.size * 5.5);
        }

        let torsoTop = this.y - this.size * 2;
        let torsoBottom = this.y - this.size * 0.2;
        
        // Head
        ctx.beginPath();
        ctx.arc(this.x, torsoTop - this.size, this.size, 0, Math.PI * 2);
        ctx.stroke();

        // Torso
        ctx.beginPath();
        ctx.moveTo(this.x, torsoTop);
        ctx.lineTo(this.x, torsoBottom);
        ctx.stroke();

        let swing = Math.sin(this.walkCycle) * 0.5; // Calmer swing

        // Legs
        let legLength = this.size * 2.2;
        ctx.beginPath();
        ctx.moveTo(this.x, torsoBottom);
        ctx.lineTo(this.x + Math.sin(swing) * legLength, torsoBottom + Math.cos(swing) * legLength);
        ctx.moveTo(this.x, torsoBottom);
        ctx.lineTo(this.x + Math.sin(-swing) * legLength, torsoBottom + Math.cos(-swing) * legLength);
        ctx.stroke();

        // Arms
        let armLength = this.size * 2.0;
        let armY = torsoTop + this.size * 0.3;
        ctx.beginPath();
        ctx.moveTo(this.x, armY);
        ctx.lineTo(this.x + Math.sin(-swing * 0.6) * armLength, armY + Math.cos(-swing * 0.6) * armLength);
        ctx.moveTo(this.x, armY);
        ctx.lineTo(this.x + Math.sin(swing * 0.6) * armLength, armY + Math.cos(swing * 0.6) * armLength);
        ctx.stroke();
    }
}

const stickmen = [
    new Stickman(200, canvas.height - 100, "#DD3333"), // Muted Red
    new Stickman(400, canvas.height - 100, "#33DD33"), // Muted Green
    new Stickman(600, canvas.height - 100, "#3333DD"), // Muted Blue
    new Stickman(800, canvas.height - 100, "#DDDD33")  // Muted Yellow
];

function handleStickmanCollisions() {
    for (let i = 0; i < stickmen.length; i++) {
        for (let j = i + 1; j < stickmen.length; j++) {
            let s1 = stickmen[i];
            let s2 = stickmen[j];
            let dx = s2.x - s1.x;
            let dy = s2.y - s1.y;
            let dist = Math.sqrt(dx * dx + dy * dy);
            let minDist = 38;
            if (dist < minDist && dist > 0) {
                let overlap = minDist - dist;
                let pushX = (dx / dist) * overlap * 0.3; // Calmer push
                
                if (s1 !== draggedStickman) s1.x -= pushX;
                if (s2 !== draggedStickman) s2.x += pushX;

                // Calmer physics interaction
                if (s1 !== draggedStickman) s1.vx -= Math.sign(pushX) * 0.6;
                if (s2 !== draggedStickman) s2.vx += Math.sign(pushX) * 0.6;

                // Activation of exclamation mark state
                s1.stateTimer = 10; // short duration
                s2.
