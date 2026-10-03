"""Demo AI chatbot for a coaching center — Fiverr portfolio sample.
Runs on free Streamlit, no API keys needed. Rule-based answers, instant reply.
"""

import re
import time

import streamlit as st

st.set_page_config(
    page_title="Bright Future Coaching — AI Assistant",
    page_icon="🎓",
    layout="centered",
)

# ---------------- clean, centered, professional styling ----------------
st.markdown(
    """
    <style>
    .block-container {
        max-width: 700px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }
    .demo-header {
        text-align: center;
        padding: 26px 18px;
        border-radius: 16px;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(30, 58, 138, .25);
    }
    .demo-header h1 { font-size: 1.5rem; margin: 0 0 6px 0; }
    .demo-header p { margin: 0; opacity: .93; font-size: .95rem; }
    .demo-badge {
        display: inline-block;
        margin-top: 10px;
        font-size: .72rem;
        letter-spacing: .04em;
        background: rgba(255, 255, 255, .18);
        padding: 4px 12px;
        border-radius: 999px;
    }
    div[data-testid="stChatInput"] {
        max-width: 700px;
        margin: 0 auto;
    }
    div[data-testid="stChatInput"] textarea {
        border-radius: 12px;
    }
    .demo-footer {
        text-align: center;
        color: #9ca3af;
        font-size: .78rem;
        margin-top: 26px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="demo-header">
        <h1>🎓 Bright Future Coaching Center</h1>
        <p>Ask me about courses, fees, batches, admission &amp; more</p>
        <span class="demo-badge">PORTFOLIO DEMO</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- knowledge base ----------------
KB = [
    {
        "keys": ["course", "courses", "subject", "offer", "teach", "class", "stream"],
        "a": "We offer **JEE (Main + Advanced)**, **NEET-UG**, **UPSC Foundation**, "
             "and **Class 11–12 (Physics, Chemistry, Maths, Biology)**. "
             "Separate batches for droppers and school-going students.",
    },
    {
        "keys": ["fee", "fees", "price", "cost", "charge", "payment", "emi"],
        "a": "Annual fees: **JEE/NEET — ₹48,000**, **UPSC Foundation — ₹36,000**, "
             "**Class 11–12 — ₹28,000**. EMI available in 4 parts, and scholarships "
             "up to 50% through our entrance test.",
    },
    {
        "keys": ["timing", "time", "batch", "batches", "schedule", "morning", "evening", "when"],
        "a": "Batches run **7 AM – 9 AM** (morning) and **4 PM – 8 PM** (evening), "
             "Monday to Saturday. New batches start on the **1st and 15th** of every month.",
    },
    {
        "keys": ["admission", "admit", "enroll", "join", "register", "process"],
        "a": "Admission is simple:\n1. Fill the form at our center or on call\n"
             "2. Take a short free level test\n3. Pay fees or the first EMI\n"
             "You can start classes within 2 days.",
    },
    {
        "keys": ["demo", "trial", "free class", "free demo"],
        "a": "Yes! We offer **2 free demo classes** for any course. "
             "Just tell us the course name and your preferred timing.",
    },
    {
        "keys": ["address", "location", "where", "reach", "contact", "phone", "number", "call"],
        "a": "Find us at **SCO 210, Sector 34, Chandigarh**. "
             "Call/WhatsApp: **+91-98765-43210** (10 AM – 7 PM).",
    },
    {
        "keys": ["faculty", "teacher", "teachers", "staff", "mentor"],
        "a": "Our faculty includes IIT/NIT alumni and doctors with **8+ years** of teaching "
             "experience. Every batch also gets a dedicated mentor.",
    },
    {
        "keys": ["result", "results", "selection", "topper", "toppers", "rank"],
        "a": "Last year: **127 JEE selections** and **89 NEET selections**, "
             "with 12 students under AIR 1000.",
    },
    {
        "keys": ["online", "live class", "recorded", "recording", "app", "internet"],
        "a": "Yes — every batch has a **live online option** with recorded backups. "
             "Online fees are 20% lower than classroom.",
    },
    {
        "keys": ["scholarship", "discount", "concession", "offer", "concession"],
        "a": "Up to **50% scholarship** through our monthly entrance test, "
             "plus 10% early-bird discount on fees paid before the 25th.",
    },
    {
        "keys": ["hostel", "pg", "stay", "room", "accommodation"],
        "a": "We help outstation students with trusted PGs near Sector 34 "
             "(₹7,000–10,000/month with food).",
    },
    {
        "keys": ["thank", "thanks", "shukriya", "dhanyavad"],
        "a": "You are most welcome! 😊 Anything else about courses, fees, or batches?",
    },
    {
        "keys": ["bye", "goodbye", "see you"],
        "a": "Goodbye and all the best for your studies! 🎓 Come back anytime.",
    },
    {
        "keys": ["hello", "hi", "hey", "namaste", "hii"],
        "a": "Hello! 👋 Ask me about **courses, fees, batches, admission, or demo classes** — I reply instantly.",
    },
]

FALLBACK = (
    "I am a demo bot, so I answer best about **courses, fees, batches, admission, "
    "demo classes, faculty, results, and contact**.\n\n"
    "Try asking: *“What are the fees for NEET?”*"
)


def answer(question: str) -> str:
    q = question.lower()
    words = set(re.findall(r"[a-z]+", q))
    best, best_score = None, 0
    for item in KB:
        score = sum(1 for k in item["keys"] if k in words or k in q)
        if score > best_score:
            best, best_score = item, score
    if best and best_score > 0:
        return best["a"]
    return FALLBACK


# ---------------- chat state ----------------
if "msgs" not in st.session_state:
    st.session_state.msgs = [
        {
            "role": "assistant",
            "content": "Namaste! 🙏 I am the assistant for **Bright Future Coaching Center**. "
                       "Ask me anything about our courses, fees, or batches.",
        }
    ]
if "pending" not in st.session_state:
    st.session_state.pending = None


def respond(text: str) -> None:
    """Append a user message + bot reply, rendering both immediately."""
    st.session_state.msgs.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.markdown(text)
    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            time.sleep(0.5)
            reply = answer(text)
            st.markdown(reply)
    st.session_state.msgs.append({"role": "assistant", "content": reply})


# ---------------- history ----------------
for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------------- suggestion chips (desktop-friendly 2x2 grid) ----------------
sugs = [
    "What courses do you offer?",
    "What are the fees?",
    "What are the batch timings?",
    "How do I take admission?",
]
r1c1, r1c2 = st.columns(2)
r2c1, r2c2 = st.columns(2)
for col, s in zip((r1c1, r1c2, r2c1, r2c2), sugs):
    if col.button(s, use_container_width=True):
        st.session_state.pending = s
        st.rerun()

# ---------------- input (centered, not edge-to-edge) ----------------
prompt = st.chat_input("Ask about courses, fees, batches...")
if st.session_state.pending:
    prompt = st.session_state.pending
    st.session_state.pending = None
if prompt:
    respond(prompt)

st.markdown(
    '<div class="demo-footer">Portfolio demo by Priyanshu • Built with Python &amp; Streamlit</div>',
    unsafe_allow_html=True,
)
