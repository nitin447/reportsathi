import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

html, body, [class*="css"]  { font-family: 'Manrope', sans-serif; }
h1, h2, h3, h4 { font-family: 'Sora', sans-serif !important; letter-spacing: -0.01em; }

/* darker, lower-contrast version of the login page's teal/blue theme —
   still animated, just easier on the eyes for longer sessions */
.stApp {
    background-color: #060f12;
    background-image:
        repeating-linear-gradient(90deg, rgba(45,212,191,0.06) 0px, rgba(45,212,191,0.06) 1.5px, transparent 1.5px, transparent 64px),
        repeating-linear-gradient(0deg, rgba(45,212,191,0.06) 0px, rgba(45,212,191,0.06) 1.5px, transparent 1.5px, transparent 64px),
        radial-gradient(circle at 15% 10%, rgba(45,212,191,0.10), transparent 55%),
        radial-gradient(circle at 90% 20%, rgba(14,165,233,0.09), transparent 55%),
        radial-gradient(circle at 30% 90%, rgba(52,211,153,0.07), transparent 55%);
    background-size: 64px 64px, 64px 64px, 200% 200%, 200% 200%, 200% 200%;
    animation: rsAppAurora 12s ease-in-out infinite;
}
@keyframes rsAppAurora {
    0%   { background-position: 0 0,     0 0,     0% 0%,   100% 20%, 20% 100%; }
    50%  { background-position: 64px 64px, 64px 64px, 30% 20%, 70% 60%,  40% 70%; }
    100% { background-position: 128px 128px, 128px 128px, 0% 0%,   100% 20%, 20% 100%; }
}

/* faint drifting watermark icons behind the content, like the login page */
.rs-app-watermark {
    position: fixed; font-size: 6.5rem; opacity: 0.03;
    pointer-events: none; z-index: 0; color: #2dd4bf;
}
.rs-app-watermark-1 { top: 6%; left: 3%; animation: rsWmDrift 26s ease-in-out infinite; }
.rs-app-watermark-2 { bottom: 5%; right: 4%; animation: rsWmDrift 30s ease-in-out infinite reverse; }
@keyframes rsWmDrift {
    0%, 100% { transform: translate(0, 0) rotate(-4deg); }
    50%      { transform: translate(16px, -20px) rotate(4deg); }
}
.rs-app-orb {
    position: fixed; border-radius: 50%; pointer-events: none; z-index: 0;
}
.rs-app-orb-1 {
    width: 6px; height: 6px; background: #2dd4bf; top: 22%; left: 6%;
    box-shadow: 0 0 30px 14px rgba(45,212,191,0.18);
    animation: rsFloat 6s ease-in-out infinite;
}
.rs-app-orb-2 {
    width: 5px; height: 5px; background: #38bdf8; bottom: 18%; right: 8%;
    box-shadow: 0 0 26px 12px rgba(56,189,248,0.16);
    animation: rsFloat 7s ease-in-out infinite 0.6s;
}
@keyframes rsFloat {
    0%, 100% { transform: translateY(0) translateX(0); }
    50%      { transform: translateY(-20px) translateX(10px); }
}

section[data-testid="stSidebar"] {
    background-color: #050e11 !important;
    background-image:
        repeating-linear-gradient(90deg, rgba(45,212,191,0.05) 0px, rgba(45,212,191,0.05) 1.5px, transparent 1.5px, transparent 48px),
        repeating-linear-gradient(0deg, rgba(45,212,191,0.05) 0px, rgba(45,212,191,0.05) 1.5px, transparent 1.5px, transparent 48px),
        radial-gradient(circle at 20% 10%, rgba(45,212,191,0.09), transparent 60%) !important;
    border-right: 1.5px solid rgba(45,212,191,0.22);
}
section[data-testid="stSidebar"] * { color: #d7ebe8 !important; }
section[data-testid="stSidebar"] a { color: #5eead4 !important; }
section[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #14b8a6, #0284c7) !important;
    border: none !important;
    color: #eafffb !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    box-shadow: 0 6px 16px rgba(20,184,166,0.25) !important;
    transition: transform 0.15s ease, box-shadow 0.2s ease;
}
section[data-testid="stSidebar"] .stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(20,184,166,0.35) !important;
}

/* sidebar brand + user card */
.rs-side-brand {
    display: flex; align-items: center; gap: 0.6rem;
    margin: 0.2rem 0 1.4rem 0;
}
.rs-side-brand-badge {
    width: 34px; height: 34px; border-radius: 9px;
    background: linear-gradient(135deg, #14b8a6, #0284c7);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    box-shadow: 0 0 0 0 rgba(20,184,166,0.4);
    animation: rsPulse 2.8s ease-out infinite;
}
.rs-side-brand-name {
    font-family: 'Sora', sans-serif; font-weight: 800; font-size: 1.05rem;
    color: #cdf4ee;
}
.rs-user-card {
    background: rgba(255,255,255,0.03);
    border: 1.5px solid rgba(45,212,191,0.28);
    border-radius: 16px; padding: 1rem 1rem 1.1rem 1rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 16px rgba(45,212,191,0.08);
    animation: rsFadeIn 0.5s ease-out;
}
.rs-avatar-row { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 0.4rem; }
.rs-avatar {
    width: 42px; height: 42px; border-radius: 50%; min-width: 42px;
    background: linear-gradient(135deg, #14b8a6, #0284c7);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Sora', sans-serif; font-weight: 800; font-size: 1.1rem;
    color: #eafffb !important;
    box-shadow: 0 0 0 3px rgba(45,212,191,0.14);
}
.rs-user-name { font-weight: 800 !important; font-size: 0.95rem; line-height: 1.2; }
.rs-user-email {
    font-size: 0.76rem !important; color: #8fb5b0 !important;
    word-break: break-all; margin-top: 0.15rem;
}

/* ---- hero card ---- */
.rs-hero {
    padding: 28px 32px; border-radius: 20px; margin-bottom: 22px;
    background: rgba(12, 32, 37, 0.6);
    border: 1.5px solid rgba(45,212,191,0.55);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 16px rgba(45,212,191,0.14);
    animation: rsFadeIn 0.5s ease-out, rsHeroGlow 4.5s ease-in-out infinite;
    position: relative; overflow: hidden;
}
.rs-hero::after {
    content: "";
    position: absolute; top: 0; left: -70%;
    width: 45%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(45,212,191,0.08), transparent);
    transform: skewX(-20deg);
    animation: rsHeroShimmer 7s ease-in-out infinite;
}
@keyframes rsHeroShimmer {
    0%   { left: -70%; }
    45%  { left: 130%; }
    100% { left: 130%; }
}
@keyframes rsHeroGlow {
    0%, 100% { border-color: rgba(45,212,191,0.55); box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 14px rgba(45,212,191,0.12); }
    50%      { border-color: rgba(56,189,248,0.55); box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 20px rgba(56,189,248,0.2); }
}
.rs-hero h1 {
    margin: 0; font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(90deg, #cdeee8, #5eead4, #cdeee8);
    background-size: 220% auto;
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 12px rgba(45,212,191,0.2);
    animation: rsShine 6s linear infinite;
    position: relative; z-index: 2;
}
@keyframes rsShine {
    0%   { background-position: 0% 50%; }
    100% { background-position: 220% 50%; }
}
.rs-hero p { margin: 6px 0 0; color: #cfe4e0; font-size: 1rem; position: relative; z-index: 2; }
.rs-pill {
    display:inline-block; padding: 4px 13px; border-radius: 999px;
    background: rgba(45,212,191,0.10); color:#5eead4; font-size:0.78rem;
    font-weight:800; letter-spacing:0.03em; margin-bottom:12px;
    border: 1px solid rgba(45,212,191,0.35);
    box-shadow: 0 0 0 0 rgba(45,212,191,0.35);
    animation: rsPulse 2.8s ease-out infinite;
    position: relative; z-index: 2;
}
@keyframes rsPulse {
    0%   { box-shadow: 0 0 0 0 rgba(45,212,191,0.35); }
    70%  { box-shadow: 0 0 0 10px rgba(45,212,191,0); }
    100% { box-shadow: 0 0 0 0 rgba(45,212,191,0); }
}

.rs-banner {
    padding: 18px 22px; border-radius: 14px; margin: 4px 0 20px;
    border-left: 5px solid var(--accent); background: var(--bg);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 5px solid var(--accent);
    animation: rsSlideUp 0.4s ease-out;
}
.rs-banner .title { font-weight:800; font-size:1.05rem; color:#f1f8f7; margin-bottom:2px; }
.rs-banner .reason { color:#c3d6d2; font-size:0.92rem; }

.rs-card {
    background: rgba(255,255,255,0.035); border: 1.5px solid rgba(45,212,191,0.22);
    border-radius: 16px; padding: 18px 20px; margin-bottom: 14px;
    animation: rsFadeIn 0.45s ease-out;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.rs-card:hover { border-color: rgba(45,212,191,0.55); transform: translateY(-2px); }
.rs-card h4 { margin:0 0 6px; font-size:1rem; color:#eef7f5; }
.rs-card .meaning { color:#bfdbd6; font-size:0.93rem; line-height:1.5; }

.rs-tag {
    display:inline-block; padding:2px 10px; border-radius:999px;
    font-size:0.72rem; font-weight:800; letter-spacing:0.03em; margin-right:8px;
}
.rs-tag.low { background:rgba(96,165,250,0.14); color:#7fb3fb; }
.rs-tag.high { background:rgba(248,113,113,0.14); color:#f19c9c; }
.rs-tag.normal { background:rgba(74,222,128,0.14); color:#79dd9a; }
.rs-tag.abnormal { background:rgba(248,113,113,0.14); color:#f19c9c; }
.rs-tag.unclear { background:rgba(250,204,21,0.14); color:#e8cf6b; }

.rs-gauge-wrap { display:flex; align-items:center; gap:14px; margin: 4px 0 2px; }
.rs-gauge-track { flex:1; height:8px; border-radius:999px; background: rgba(255,255,255,0.06); position:relative; overflow:hidden; }
.rs-gauge-fill { height:100%; border-radius:999px; animation: rsGrow 0.7s ease-out; }
.rs-gauge-label { font-size:0.78rem; color:#8fada8; min-width:70px; text-align:right; }

.rs-dot { margin: 8px 0; padding-left: 14px; border-left: 2px solid rgba(45,212,191,0.35); color:#bfdbd6; }

.rs-chat-user {
    background: rgba(45,212,191,0.09); border: 1px solid rgba(45,212,191,0.28);
    border-radius: 14px 14px 4px 14px;
    padding: 10px 14px; margin: 6px 0 6px auto; max-width: 85%; color:#dff5f0;
    animation: rsSlideUp 0.3s ease-out;
}
.rs-chat-ai {
    background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px 14px 14px 4px; padding: 12px 16px; margin: 6px 0;
    max-width: 92%; color:#dbeeeb; animation: rsSlideUp 0.3s ease-out;
}

@keyframes rsFadeIn { from {opacity:0; transform: translateY(6px);} to {opacity:1; transform:none;} }
@keyframes rsSlideUp { from {opacity:0; transform: translateY(10px);} to {opacity:1; transform:none;} }
@keyframes rsGrow { from {width:0%;} }

section[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 16px !important; border: 1.5px dashed rgba(45,212,191,0.35) !important;
    transition: border-color 0.2s ease, background 0.2s ease;
}
section[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(45,212,191,0.6) !important;
    background: rgba(45,212,191,0.04) !important;
}
[data-testid="stFileUploaderDropzone"] * { color: #bfdbd6 !important; }

.stButton>button, .stFormSubmitButton>button, [data-testid="stFormSubmitButton"] button {
    border-radius: 12px; font-weight: 800; height: 2.9rem;
    transition: transform 0.15s ease, box-shadow 0.2s ease;
    background: linear-gradient(135deg, #14b8a6, #0284c7) !important;
    background-size: 200% 200% !important;
    animation: rsGradShift 6s ease infinite !important;
    color: #eafffb !important;
    border: none !important;
    box-shadow: 0 8px 20px rgba(20,184,166,0.3) !important;
}
.stButton>button:hover, .stFormSubmitButton>button:hover, [data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 26px rgba(20,184,166,0.4) !important;
}
@keyframes rsGradShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stButton>button:disabled, .stButton>button:disabled:hover {
    background: rgba(255,255,255,0.05) !important;
    color: #56655f !important;
    box-shadow: none !important;
    border: 1.5px dashed rgba(255,255,255,0.12) !important;
    animation: none !important;
    transform: none !important;
    cursor: not-allowed;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.3rem !important; border-bottom: none !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px solid rgba(45,212,191,0.3) !important;
    border-radius: 12px !important;
    padding: 0.3rem !important;
    width: fit-content !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
}
.stTabs [data-baseweb="tab"] {
    font-weight: 700; color: #a9c9c4;
    border-radius: 9px !important;
    padding: 0.45rem 1.1rem !important;
    margin: 0 !important;
    background: transparent !important;
    overflow: hidden !important;
    transition: color 0.2s ease, background 0.2s ease;
    white-space: nowrap;
}
.stTabs [aria-selected="true"] {
    color: #052024 !important;
    background: linear-gradient(90deg, #2dd4bf, #38bdf8) !important;
    border-radius: 9px !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 0.8rem !important; }

.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px solid rgba(45,212,191,0.3) !important;
    border-radius: 10px !important;
    color: #eef7f5 !important;
}
.stTextInput input {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px solid rgba(45,212,191,0.3) !important;
    color: #eef7f5 !important;
    border-radius: 10px !important;
}

/* body text — bright enough to read, not glaring white */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
.stCaption, [data-testid="stCaptionContainer"] {
    color: #cfe4e0 !important;
}
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h4 {
    color: #eef7f5 !important;
    font-weight: 800 !important;
}
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px solid rgba(45,212,191,0.22) !important;
    border-radius: 12px !important;
}
</style>

<div class="rs-app-orb rs-app-orb-1"></div>
<div class="rs-app-orb rs-app-orb-2"></div>
<div class="rs-app-watermark rs-app-watermark-1">🩺</div>
<div class="rs-app-watermark rs-app-watermark-2">➕</div>
"""

URGENCY_STYLE = {
    "urgent": ("#EF4444", "rgba(239,68,68,0.08)", "Seek medical attention"),
    "see_doctor_soon": ("#F59E0B", "rgba(245,158,11,0.08)", "See a doctor soon"),
    "routine_followup": ("#38BDF8", "rgba(56,189,248,0.08)", "Discuss at your next visit"),
    "all_normal": ("#4ADE80", "rgba(74,222,128,0.08)", "Nothing outside the normal range"),
}


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def hero():
    st.markdown(
        '<div class="rs-hero"><span class="rs-pill">AI HEALTH COMPANION</span>'
        '<h1>ReportSathi</h1>'
        '<p>Understand your medical reports, in your language.</p></div>',
        unsafe_allow_html=True,
    )


def urgency_banner(level: str, reason: str):
    accent, bg, title = URGENCY_STYLE.get(level, URGENCY_STYLE["routine_followup"])
    st.markdown(
        f'<div class="rs-banner" style="--accent:{accent};--bg:{bg}">'
        f'<div class="title">{title}</div><div class="reason">{reason}</div></div>',
        unsafe_allow_html=True,
    )


def key_point_card(name: str, status: str, meaning: str, deviation_pct=None):
    tag_class = status if status in ("low", "high", "normal", "abnormal", "unclear") else "unclear"
    gauge = ""
    if deviation_pct is not None:
        pct = min(100, max(6, deviation_pct))
        color = "#f19c9c" if status == "high" else "#7fb3fb"
        gauge = (
            '<div class="rs-gauge-wrap"><div class="rs-gauge-track">'
            f'<div class="rs-gauge-fill" style="width:{pct}%;background:{color}"></div></div>'
            f'<div class="rs-gauge-label">{deviation_pct}% off range</div></div>'
        )
    st.markdown(
        f'<div class="rs-card"><span class="rs-tag {tag_class}">{status.upper()}</span>'
        f'<h4 style="display:inline">{name}</h4>{gauge}'
        f'<div class="meaning">{meaning}</div></div>',
        unsafe_allow_html=True,
    )


def dot(text: str):
    st.markdown(f'<div class="rs-dot">{text}</div>', unsafe_allow_html=True)


def chat_bubble(role: str, text: str):
    cls = "rs-chat-user" if role == "user" else "rs-chat-ai"
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)