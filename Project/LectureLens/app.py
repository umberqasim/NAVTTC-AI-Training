import streamlit as st
import re
from summariser import get_transcript, generate_summary, generate_quiz
from database import init_db, save_result, get_history

init_db()

st.set_page_config(
    page_title="LectureLens AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ── GLOBAL STYLE OVERRIDES ── */
    * { 
        font-family: 'Inter', sans-serif; 
    }
    
    h1, h2, h3, h4, h5, h6 { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        font-weight: 700 !important;
        color: #f8fafc !important;
    }

    .stApp { 
        background: #05050a; 
    }

    /* ── SIDEBAR STYLE ── */
    section[data-testid="stSidebar"] {
        background: #020205;
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 0rem;
    }

    .brand-block {
        padding: 2rem 0 1.5rem 0;
        border-bottom: 1px solid rgba(99, 102, 241, 0.1);
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .brand-icon-wrap {
        width: 60px; height: 60px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.8rem; margin: 0 auto 0.8rem auto;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .brand-block:hover .brand-icon-wrap {
        transform: translateY(-3px) rotate(5deg);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.6);
    }
    .brand-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.3rem; font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -0.01em;
    }
    .brand-tagline { 
        font-size: 0.68rem; 
        font-weight: 700;
        color: #818cf8 !important; 
        letter-spacing: 0.1em; 
        text-transform: uppercase; 
        margin-top: 0.25rem; 
    }

    .section-lbl {
        font-size: 0.62rem; font-weight: 800;
        color: #475569 !important;
        letter-spacing: 0.15em; text-transform: uppercase;
        padding: 1.2rem 0 0.4rem 0;
    }

    .nav-btn {
        display: flex; align-items: center; gap: 0.75rem;
        padding: 0.75rem 1rem; border-radius: 12px;
        margin: 0.3rem 0; font-size: 0.85rem;
        font-weight: 600; color: #64748b !important;
        border: 1px solid transparent; cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        background: rgba(255, 255, 255, 0.01);
    }
    .nav-btn:hover {
        background: rgba(99, 102, 241, 0.05);
        border-color: rgba(99, 102, 241, 0.15);
        color: #cbd5e1 !important;
        transform: translateX(4px);
    }
    .nav-btn.active {
        background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(139,92,246,0.12));
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #c7d2fe !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.05);
    }
    .nav-icon { font-size: 1.05rem; }
    .nav-badge {
        margin-left: auto; background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white; border-radius: 99px;
        padding: 0.15rem 0.55rem; font-size: 0.65rem; font-weight: 800;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.35);
    }

    .mini-stat {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(99, 102, 241, 0.12);
        border-radius: 12px; padding: 0.8rem 1rem;
        margin: 0.4rem 0; display: flex;
        justify-content: space-between; align-items: center;
        transition: all 0.2s ease;
    }
    .mini-stat:hover {
        border-color: rgba(99, 102, 241, 0.25);
        background: rgba(15, 23, 42, 0.6);
    }
    .mini-stat-lbl { font-size: 0.75rem; color: #64748b !important; font-weight: 500; }
    .mini-stat-val { font-size: 1.05rem; font-weight: 700; font-family: 'Fira Code', monospace; }

    .hint-box {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 12px; padding: 1rem;
        margin-top: 1.5rem; font-size: 0.75rem;
        line-height: 1.8;
        backdrop-filter: blur(8px);
    }
    .hint-box .ok  { color: #10b981 !important; font-weight: bold; }
    .hint-box .no  { color: #f43f5e !important; font-weight: bold; }

    /* ── TOPBAR STYLE ── */
    .topbar {
        background: rgba(10, 10, 20, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 16px;
        padding: 1.2rem 1.8rem;
        display: flex; align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .topbar-left { display: flex; align-items: center; gap: 1.2rem; }
    .topbar-title { 
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.3rem; font-weight: 800; 
        background: linear-gradient(135deg, #ffffff, #c7d2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .topbar-sub   { font-size: 0.8rem; color: #64748b; margin-top: 0.2rem; }
    .topbar-right { display: flex; align-items: center; gap: 0.75rem; }
    
    .pill {
        display: inline-flex; align-items: center; gap: 0.45rem;
        padding: 0.4rem 1rem; border-radius: 99px;
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .pill-green { 
        background: rgba(16, 185, 129, 0.08); 
        border: 1px solid rgba(16, 185, 129, 0.25); 
        color: #34d399; 
    }
    .pill-indigo { 
        background: rgba(99, 102, 241, 0.08); 
        border: 1px solid rgba(99, 102, 241, 0.25); 
        color: #a5b4fc; 
    }
    .pill-dot { 
        width: 6px; height: 6px; border-radius: 50%; 
        box-shadow: 0 0 8px currentColor;
    }

    /* ── STAT CARDS ── */
    .cards-grid {
        display: grid; grid-template-columns: repeat(5, 1fr);
        gap: 1rem; margin-bottom: 2rem;
    }
    .kard {
        border-radius: 16px; padding: 1.25rem 1.1rem;
        position: relative; overflow: hidden;
        border: 1px solid;
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .kard:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.5);
    }
    .kard::before {
        content:''; position: absolute;
        top: -25px; right: -25px;
        width: 80px; height: 80px; border-radius: 50%;
        opacity: 0.1;
        transition: all 0.3s ease;
    }
    .kard:hover::before {
        transform: scale(1.2);
        opacity: 0.18;
    }
    
    .kard.indigo { border-color: rgba(99, 102, 241, 0.2); }
    .kard.indigo:hover { border-color: rgba(99, 102, 241, 0.5); box-shadow: 0 0 20px rgba(99, 102, 241, 0.15); }
    .kard.indigo::before { background: #6366f1; }
    
    .kard.green  { border-color: rgba(16, 185, 129, 0.2); }
    .kard.green:hover { border-color: rgba(16, 185, 129, 0.5); box-shadow: 0 0 20px rgba(16, 185, 129, 0.15); }
    .kard.green::before  { background: #10b981; }
    
    .kard.red    { border-color: rgba(244, 63, 94, 0.2); }
    .kard.red:hover { border-color: rgba(244, 63, 94, 0.5); box-shadow: 0 0 20px rgba(244, 63, 94, 0.15); }
    .kard.red::before    { background: #f43f5e; }
    
    .kard.yellow { border-color: rgba(245, 158, 11, 0.2); }
    .kard.yellow:hover { border-color: rgba(245, 158, 11, 0.5); box-shadow: 0 0 20px rgba(245, 158, 11, 0.15); }
    .kard.yellow::before { background: #f59e0b; }
    
    .kard.purple { border-color: rgba(168, 85, 247, 0.2); }
    .kard.purple:hover { border-color: rgba(168, 85, 247, 0.5); box-shadow: 0 0 20px rgba(168, 85, 247, 0.15); }
    .kard.purple::before { background: #a855f7; }

    .kard-icon { font-size: 1.4rem; margin-bottom: 0.6rem; display: inline-block; }
    .kard-val  { font-size: 2rem; font-weight: 800; line-height: 1; font-family: 'Fira Code', monospace; }
    .kard-lbl  { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.5rem; color: #64748b; }
    .kard-sub  { font-size: 0.72rem; margin-top: 0.25rem; font-weight: 500; }
    .kard-bar  { height: 4px; border-radius: 2px; margin-top: 1rem; opacity: 0.85; transition: width 0.5s ease; }

    .kard.indigo .kard-val { color: #818cf8; }
    .kard.indigo .kard-bar { background: linear-gradient(90deg, #6366f1, #8b5cf6); }
    .kard.indigo .kard-sub { color: #64748b; }
    
    .kard.green  .kard-val { color: #34d399; }
    .kard.green  .kard-bar { background: linear-gradient(90deg, #10b981, #059669); }
    .kard.green  .kard-sub { color: #34d399; }
    
    .kard.red    .kard-val { color: #fb7185; }
    .kard.red    .kard-bar { background: linear-gradient(90deg, #f43f5e, #be123c); }
    .kard.red    .kard-sub { color: #fb7185; }
    
    .kard.yellow .kard-val { color: #fbbf24; }
    .kard.yellow .kard-bar { background: linear-gradient(90deg, #f59e0b, #d97706); }
    .kard.yellow .kard-sub { color: #fbbf24; }
    
    .kard.purple .kard-val { color: #c084fc; }
    .kard.purple .kard-bar { background: linear-gradient(90deg, #a855f7, #7e22ce); }
    .kard.purple .kard-sub { color: #c084fc; }

    /* ── ST CONTAINER STYLING ── */
    div[data-testid="stVerticalBlockBorderWrapper"], 
    div[class*="stVerticalBlockBorderWrapper"] {
        background: rgba(12, 12, 28, 0.4) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        border-radius: 16px !important;
        padding: 1.8rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 10px 30px -15px rgba(0, 0, 0, 0.5) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"],
    div[class*="stVerticalBlockBorderWrapper"] div[class*="stVerticalBlockBorderWrapper"] {
        background: rgba(18, 18, 36, 0.35) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 1.4rem !important;
        margin: 0.8rem 0 !important;
        box-shadow: none !important;
    }

    .zone-header {
        display: flex; align-items: center; gap: 0.8rem;
        margin-bottom: 1.2rem;
    }
    .zone-dot { 
        width: 8px; height: 8px; border-radius: 50%; 
        background: #6366f1; 
        box-shadow: 0 0 12px #6366f1, 0 0 4px #6366f1;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse {
        0% { transform: scale(0.9); opacity: 0.6; }
        100% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 16px #6366f1, 0 0 6px #6366f1; }
    }
    .zone-title { font-size: 0.8rem; font-weight: 700; color: #a5b4fc !important; letter-spacing: 0.08em; text-transform: uppercase; }
    .zone-line { flex:1; height:1px; background: linear-gradient(90deg, rgba(99,102,241,0.2), transparent); }

    .stTextInput > div > div > input {
        background: #090915 !important;
        border: 1px solid rgba(99,102,241,0.25) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-size: 0.95rem !important;
        padding: 0.8rem 1.1rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(99,102,241,0.7) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
        background: #0f0f25 !important;
    }
    .stTextInput > div > div > input::placeholder { color: #3b3b64 !important; }
    .stTextInput label { 
        color: #a5b4fc !important; 
        font-size: 0.85rem !important; 
        font-weight: 600 !important; 
        margin-bottom: 0.5rem !important; 
        letter-spacing: 0.01em !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #6366f1, #7c3aed) !important;
        border: none !important;
        border-radius: 12px !important; 
        padding: 0.85rem 1.5rem !important;
        font-size: 0.95rem !important; 
        width: 100% !important; 
        letter-spacing: 0.05em !important;
        box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-family: 'Fira Code', monospace !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
        background: linear-gradient(135deg, #5b52f9, #7275ff, #8b4eff) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    .stButton > button * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* ── PROCESS BANNER ── */
    .proc-banner {
        background: rgba(99, 102, 241, 0.06);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-left: 4px solid #6366f1;
        border-radius: 12px; padding: 1.1rem 1.4rem;
        margin-bottom: 1.5rem;
        display: flex; align-items: center; gap: 1.2rem;
        animation: fadeIn 0.4s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .proc-text { font-size: 0.88rem; font-weight: 700; color: #a5b4fc; letter-spacing: 0.02em; }
    .proc-sub  { font-size: 0.78rem; color: #64748b; margin-top: 0.25rem; }
    .proc-tags { margin-left:auto; display:flex; gap:0.5rem; }
    .ptag {
        padding: 0.25rem 0.75rem; border-radius: 6px;
        font-size: 0.65rem; font-weight: 700;
        font-family: 'Fira Code', monospace;
        letter-spacing: 0.02em;
    }
    .ptag-i { background: rgba(99,102,241,0.15); color: #c7d2fe; border: 1px solid rgba(99,102,241,0.3); }
    .ptag-g { background: rgba(16,185,129,0.15);  color: #a7f3d0;  border: 1px solid rgba(16,185,129,0.3); }

    /* ── RESULTS & PANEL ── */
    .res-header {
        display: flex; align-items: center; gap: 0.8rem;
        margin: 2.2rem 0 1rem 0;
    }
    .res-dot { width: 8px; height: 8px; border-radius: 50%; }
    .res-title { font-size: 0.85rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }
    .res-line { flex:1; height:1px; background: rgba(255, 255, 255, 0.08); }
    .res-badge {
        font-size: 0.65rem; padding: 0.25rem 0.75rem;
        border-radius: 6px; font-weight: 700;
        font-family: 'Fira Code', monospace;
        letter-spacing: 0.02em;
    }

    /* ── INTERACTIVE QUIZ ── */
    .q-counter {
        font-size: 0.68rem; font-weight: 700;
        color: #818cf8; letter-spacing: 0.1em;
        font-family: 'Fira Code', monospace;
        margin-bottom: 0.6rem;
    }
    .q-text { 
        font-size: 0.95rem; font-weight: 600; 
        color: #f1f5f9; margin-bottom: 1.2rem; 
        line-height: 1.5; 
    }

    .score-wrap {
        background: linear-gradient(135deg, rgba(99,102,241,0.06), rgba(168,85,247,0.06));
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 16px; padding: 1.5rem 1.8rem;
        display: flex; align-items: center;
        justify-content: space-between; margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(99,102,241,0.08);
    }
    .score-num { font-size: 2.8rem; font-weight: 800; font-family: 'Fira Code', monospace; line-height: 1; }
    .score-pct { font-size: 0.8rem; color: #64748b; margin-top: 0.4rem; font-weight: 500; }
    .score-tag {
        padding: 0.6rem 1.4rem; border-radius: 10px;
        font-size: 0.8rem; font-weight: 800;
        letter-spacing: 0.08em; font-family: 'Fira Code', monospace;
        text-transform: uppercase;
    }

    /* ── TABS & WIDGET INTERFACES ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 23, 42, 0.6) !important; 
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important; 
        padding: 6px !important; 
        gap: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600 !important; 
        font-size: 0.95rem !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
        border-radius: 8px !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab"]:hover * {
        color: #ffffff !important;
    }

    div[data-testid="stExpander"] {
        background: rgba(12, 12, 24, 0.4) !important; 
        border: 1px solid rgba(255, 255, 255, 0.05) !important; 
        border-radius: 12px !important;
        box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 0.8rem !important;
    }
    div[data-testid="stExpander"] summary { 
        color: #c7d2fe !important; 
        font-weight: 600 !important; 
        font-size: 0.92rem !important;
    }
    div[data-testid="stExpander"] summary:hover { 
        color: #ffffff !important; 
    }

    .stSuccess > div { 
        background: rgba(16,185,129,0.05) !important; 
        border: 1px solid rgba(16,185,129,0.2) !important; 
        border-radius: 10px !important; 
        color: #34d399 !important;
    }
    .stError   > div { 
        background: rgba(244,63,94,0.05) !important; 
        border: 1px solid rgba(244,63,94,0.2) !important; 
        border-radius: 10px !important; 
        color: #fb7185 !important;
    }
    .stWarning > div { 
        background: rgba(245,158,11,0.05) !important; 
        border: 1px solid rgba(245,158,11,0.2) !important; 
        border-radius: 10px !important; 
        color: #fbbf24 !important;
    }

    div[data-testid="stStatusWidget"] {
        background: #090915 !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
    }

    p  { color: #94a3b8; }
    li { color: #94a3b8; }
    strong { color: #c7d2fe !important; }
    .stMarkdown p { color: #94a3b8; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #05050a; }
    ::-webkit-scrollbar-thumb { background: #4f46e5; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #6366f1; }

    /* ── HISTORY READ-ONLY QUIZ LABEL ── */
    .readonly-label {
        display: inline-flex; align-items: center; gap: 0.4rem;
        background: rgba(99,102,241,0.08);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 8px; padding: 0.3rem 0.8rem;
        font-size: 0.68rem; font-weight: 700;
        color: #a5b4fc; letter-spacing: 0.08em;
        font-family: 'Fira Code', monospace;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)


def parse_quiz(quiz_text):
    questions = []
    blocks = re.split(r'\n(?=Q\d+:)', quiz_text.strip())
    for block in blocks:
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        q = {}
        for line in lines:
            if re.match(r'Q\d+:', line):
                q['question'] = re.sub(r'Q\d+:\s*', '', line)
            elif line.startswith('A:'):
                q['A'] = line[2:].strip()
            elif line.startswith('B:'):
                q['B'] = line[2:].strip()
            elif line.startswith('C:'):
                q['C'] = line[2:].strip()
            elif line.startswith('D:'):
                q['D'] = line[2:].strip()
            elif line.startswith('ANSWER:'):
                q['answer'] = line.replace('ANSWER:', '').strip()
            elif line.startswith('EXPLANATION:'):
                q['explanation'] = line.replace('EXPLANATION:', '').strip()
        if 'question' in q and 'answer' in q:
            questions.append(q)
    return questions


# ── INTERACTIVE QUIZ (Live Monitor) ──
def render_quiz(questions, key_prefix="main"):
    if f"{key_prefix}_answers" not in st.session_state:
        st.session_state[f"{key_prefix}_answers"] = {}
    if f"{key_prefix}_submitted" not in st.session_state:
        st.session_state[f"{key_prefix}_submitted"] = False

    answers   = st.session_state[f"{key_prefix}_answers"]
    submitted = st.session_state[f"{key_prefix}_submitted"]

    if submitted:
        score = sum(1 for i, q in enumerate(questions) if answers.get(i) == q['answer'])
        pct   = int((score / len(questions)) * 100)
        if pct >= 70:
            col, bg, txt = "#34d399", "rgba(16,185,129,0.08)", "PASS"
        elif pct >= 40:
            col, bg, txt = "#fbbf24", "rgba(245,158,11,0.08)", "AVERAGE"
        else:
            col, bg, txt = "#fb7185", "rgba(244,63,94,0.08)", "FAIL"
        st.markdown(f"""
        <div class="score-wrap">
            <div>
                <div class="score-num" style="color:{col}">{score}/{len(questions)}</div>
                <div class="score-pct">Score — {pct}% Correct</div>
            </div>
            <div class="score-tag" style="background:{bg};color:{col};border:1px solid {col}50">{txt}</div>
        </div>""", unsafe_allow_html=True)

    for i, q in enumerate(questions):
        with st.container(border=True):
            st.markdown(f'<div class="q-counter">QUESTION {i+1} / {len(questions)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)

            if not submitted:
                choice = st.radio(
                    f"q_{key_prefix}_{i}",
                    options=["A","B","C","D"],
                    format_func=lambda x, q=q: f"{x})  {q.get(x,'')}",
                    key=f"radio_{key_prefix}_{i}",
                    label_visibility="collapsed"
                )
                answers[i] = choice
            else:
                correct = q['answer']
                user    = answers.get(i, "")
                for opt in ["A","B","C","D"]:
                    txt = f"{opt})  {q.get(opt,'')}"
                    if opt == correct:
                        st.success(f"✅  {txt}")
                    elif opt == user and user != correct:
                        st.error(f"❌  {txt}")
                    else:
                        st.markdown(f"<p style='color:#64748b;margin:0.25rem 0;font-size:0.86rem'>　　{txt}</p>", unsafe_allow_html=True)
                if 'explanation' in q:
                    st.markdown(f"""<div style='background:rgba(245,158,11,0.04);border:1px solid rgba(245,158,11,0.25);
                    border-radius:10px;padding:0.75rem 1rem;margin-top:0.75rem;font-size:0.8rem;color:#fbbf24;line-height:1.5'>
                    💡 {q['explanation']}</div>""", unsafe_allow_html=True)

    st.session_state[f"{key_prefix}_answers"] = answers
    if not submitted:
        if st.button("✅  SUBMIT QUIZ", key=f"submit_{key_prefix}", type="primary"):
            st.session_state[f"{key_prefix}_submitted"] = True
            st.rerun()
    else:
        if st.button("🔄  RETRY QUIZ", key=f"retry_{key_prefix}"):
            st.session_state[f"{key_prefix}_answers"]  = {}
            st.session_state[f"{key_prefix}_submitted"] = False
            st.rerun()


# ── READ-ONLY QUIZ (History Log) ──
def render_quiz_readonly(questions):
    st.markdown('<div class="readonly-label">📋 Quiz Answer Key</div>', unsafe_allow_html=True)
    for i, q in enumerate(questions):
        with st.container(border=True):
            st.markdown(f'<div class="q-counter">QUESTION {i+1} / {len(questions)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            correct = q['answer']
            for opt in ["A", "B", "C", "D"]:
                txt = f"{opt})  {q.get(opt, '')}"
                if opt == correct:
                    st.success(f"✅  {txt}")
                else:
                    st.markdown(f"<p style='color:#64748b;margin:0.25rem 0;font-size:0.86rem'>　　{txt}</p>", unsafe_allow_html=True)
            if 'explanation' in q:
                st.markdown(f"""<div style='background:rgba(245,158,11,0.04);border:1px solid rgba(245,158,11,0.25);
                border-radius:10px;padding:0.75rem 1rem;margin-top:0.75rem;font-size:0.8rem;color:#fbbf24;line-height:1.5'>
                💡 {q['explanation']}</div>""", unsafe_allow_html=True)


# ── SIDEBAR ──
with st.sidebar:
    history_data = get_history()
    total = len(history_data)
    st.markdown(f"""
    <div class="brand-block">
        <div class="brand-icon-wrap">🎓</div>
        <div class="brand-name">LectureLens</div>
        <div class="brand-tagline">AI Learning Intelligence</div>
    </div>
    <div class="section-lbl">Navigation</div>
    <div class="nav-btn active"><span class="nav-icon">⚡</span> Live Monitor</div>
    <div class="nav-btn"><span class="nav-icon">📋</span> Summary Log</div>
    <div class="nav-btn"><span class="nav-icon">🧠</span> Quiz Engine</div>
    <div class="nav-btn"><span class="nav-icon">🕓</span> History <span class="nav-badge">{total}</span></div>
    <div class="section-lbl" style="margin-top:1rem">Session Stats</div>
    <div class="mini-stat">
        <div class="mini-stat-lbl">📚 Videos Processed</div>
        <div class="mini-stat-val" style="color:#818cf8">{total}</div>
    </div>
    <div class="mini-stat">
        <div class="mini-stat-lbl">🧠 Quizzes Generated</div>
        <div class="mini-stat-val" style="color:#4ade80">{total}</div>
    </div>
    <div class="mini-stat">
        <div class="mini-stat-lbl">🎯 Questions/Quiz</div>
        <div class="mini-stat-val" style="color:#fbbf24">10</div>
    </div>
    <div class="mini-stat">
        <div class="mini-stat-lbl">⚡ AI Engine</div>
        <div class="mini-stat-val" style="color:#c084fc;font-size:0.82rem">GROQ ACTIVE</div>
    </div>
    <div class="hint-box">
        <span class="ok">✅</span> &nbsp;Original captions — supported<br>
        <span class="ok">✅</span> &nbsp;Auto-generated — supported<br>
        <span class="no">✅</span> &nbsp;Auto-dubbed — supported<br>
        <span class="no">❌</span> &nbsp;Captions disabled — not supported
    </div>
    """, unsafe_allow_html=True)


# ── MAIN ──
history_data = get_history()
total = len(history_data)

st.markdown(f"""
<div class="topbar">
    <div class="topbar-left">
        <div style="width:42px;height:42px;background:linear-gradient(135deg,#6366f1,#8b5cf6);
        border-radius:12px;display:flex;align-items:center;justify-content:center;
        font-size:1.30rem;box-shadow:0 6px 20px rgba(99,102,241,0.35)">🎓</div>
        <div>
            <div class="topbar-title">Live Monitor — LectureLens</div>
            <div class="topbar-sub">AI-Powered Lecture Summarisation & Quiz Generation Platform</div>
        </div>
    </div>
    <div class="topbar-right">
        <div class="pill pill-green"><div class="pill-dot" style="background:#4ade80"></div>AI Engine Active</div>
        <div class="pill pill-indigo"><div class="pill-dot" style="background:#818cf8"></div>Groq Enforced</div>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⚡  Live Monitor", "🕓  History Log"])

with tab1:
    st.markdown(f"""
    <div class="cards-grid">
        <div class="kard indigo">
            <div class="kard-icon">📊</div>
            <div class="kard-val">{total}</div>
            <div class="kard-lbl">Total Videos</div>
            <div class="kard-sub">This session</div>
            <div class="kard-bar" style="width:70%"></div>
        </div>
        <div class="kard green">
            <div class="kard-icon">✅</div>
            <div class="kard-val">{total}</div>
            <div class="kard-lbl">Summaries</div>
            <div class="kard-sub">AI verified</div>
            <div class="kard-bar" style="width:100%"></div>
        </div>
        <div class="kard red">
            <div class="kard-icon">🧠</div>
            <div class="kard-val">{total}</div>
            <div class="kard-lbl">Quizzes</div>
            <div class="kard-sub">↑ {total} done</div>
            <div class="kard-bar" style="width:85%"></div>
        </div>
        <div class="kard yellow">
            <div class="kard-icon">⚡</div>
            <div class="kard-val" style="font-size:1.2rem">LIVE</div>
            <div class="kard-lbl">Engine Status</div>
            <div class="kard-sub">Groq LLaMA 3.3</div>
            <div class="kard-bar" style="width:100%"></div>
        </div>
        <div class="kard purple">
            <div class="kard-icon">🎯</div>
            <div class="kard-val">10</div>
            <div class="kard-lbl">Questions</div>
            <div class="kard-sub">Per lecture</div>
            <div class="kard-bar" style="width:75%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("""
        <div class="zone-header">
            <div class="zone-dot"></div>
            <div class="zone-title">Lecture URL Input</div>
            <div class="zone-line"></div>
        </div>
        """, unsafe_allow_html=True)
        url = st.text_input("🔗  YouTube Lecture URL", placeholder="https://www.youtube.com/watch?v=...")
        generate_btn = st.button("⚡  GENERATE SUMMARY & QUIZ", type="primary")

    if generate_btn:
        if not url.strip():
            st.warning("⚠️ Please enter a YouTube URL first.")
        else:
            st.markdown("""
            <div class="proc-banner">
                <div>⚡</div>
                <div>
                    <div class="proc-text">PROCESSING LECTURE — AI ENGINE ACTIVE</div>
                    <div class="proc-sub">Fetching transcript · Generating summary · Building quiz</div>
                </div>
                <div class="proc-tags">
                    <div class="ptag ptag-i">GROQ AI</div>
                    <div class="ptag ptag-g">LIVE</div>
                </div>
            </div>""", unsafe_allow_html=True)

            with st.status("⚙️ Processing...", expanded=True) as status:
                st.write("📥 Fetching transcript...")
                try:
                    transcript = get_transcript(url)
                    st.write("✅ Transcript fetched!")
                    st.write("🤖 Generating summary...")
                    summary = generate_summary(transcript)
                    st.write("✅ Summary ready!")
                    st.write("🧠 Generating quiz...")
                    quiz = generate_quiz(transcript)
                    st.write("✅ Quiz ready!")
                    save_result(url, summary, quiz)
                    status.update(label="✅ ANALYSIS COMPLETE", state="complete")
                    st.session_state["current_summary"] = summary
                    st.session_state["current_quiz"]    = quiz
                    st.session_state["main_answers"]    = {}
                    st.session_state["main_submitted"]  = False
                except ValueError as e:
                    st.error(str(e))
                    status.update(label="❌ FAILED", state="error")
                    st.stop()

    if "current_summary" in st.session_state:
        st.markdown("""
        <div class="res-header">
            <div class="res-dot" style="background:#4ade80;box-shadow:0 0 8px #22c55e"></div>
            <div class="res-title" style="color:#4ade80">Lecture Summary</div>
            <div class="res-line"></div>
            <div class="res-badge" style="background:rgba(34,197,94,0.1);color:#4ade80;border:1px solid rgba(34,197,94,0.2)">AI GENERATED</div>
        </div>""", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(st.session_state["current_summary"])

        st.markdown("""
        <div class="res-header">
            <div class="res-dot" style="background:#c084fc;box-shadow:0 0 8px #a855f7"></div>
            <div class="res-title" style="color:#c084fc">Practice Quiz</div>
            <div class="res-line"></div>
            <div class="res-badge" style="background:rgba(168,85,247,0.1);color:#c084fc;border:1px solid rgba(168,85,247,0.2)">INTERACTIVE</div>
        </div>""", unsafe_allow_html=True)
        with st.container(border=True):
            questions = parse_quiz(st.session_state["current_quiz"])
            if questions:
                render_quiz(questions, key_prefix="main")
            else:
                st.markdown(st.session_state["current_quiz"])

# ── HISTORY TAB ──
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    history_data = get_history()
    if not history_data:
        st.markdown("""
        <div style="text-align:center;padding:4rem">
            <div style="font-size:3.5rem">📭</div>
            <h3 style="color:#475569;margin-top:1rem">No history yet</h3>
            <p style="color:#334155">Generate your first summary to see it here!</p>
        </div>""", unsafe_allow_html=True)
    else:
        for record in history_data:
            id, url, summary, quiz, created_at = record
            with st.expander(f"📌  {url[:65]}...   |   🕓 {created_at}"):
                st.markdown(summary)
                st.divider()
                st.markdown("""
                <div class="res-header">
                    <div class="res-dot" style="background:#c084fc;box-shadow:0 0 8px #a855f7"></div>
                    <div class="res-title" style="color:#c084fc">Quiz Answer Key</div>
                    <div class="res-line"></div>
                    <div class="res-badge" style="background:rgba(168,85,247,0.1);color:#c084fc;border:1px solid rgba(168,85,247,0.2)">READ ONLY</div>
                </div>""", unsafe_allow_html=True)
                questions = parse_quiz(quiz)
                if questions:
                    render_quiz_readonly(questions)
                else:
                    st.markdown(quiz)
