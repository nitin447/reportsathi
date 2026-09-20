"""
auth_ui.py — ReportSathi login/signup screen
Style: dark teal/blue "medical-tech" theme — scrolling grid background,
aurora glow blobs, animated ECG heartbeat line, glass card with a bold
pulsing teal border, glowing gradient text, and a conversational tone.
"""

import streamlit as st
from src.auth import signup, login, find_or_create_google_user


def _login_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 620px !important;
        }
        header[data-testid="stHeader"] { background: transparent; }

        .stApp {
            background-color: #0a1a20;
            background-image:
                repeating-linear-gradient(90deg, rgba(45,212,191,0.10) 0px, rgba(45,212,191,0.10) 1.5px, transparent 1.5px, transparent 64px),
                repeating-linear-gradient(0deg, rgba(45,212,191,0.10) 0px, rgba(45,212,191,0.10) 1.5px, transparent 1.5px, transparent 64px),
                radial-gradient(circle at 20% 15%, rgba(45,212,191,0.22), transparent 55%),
                radial-gradient(circle at 82% 30%, rgba(14,165,233,0.20), transparent 55%),
                radial-gradient(circle at 30% 88%, rgba(52,211,153,0.16), transparent 55%),
                radial-gradient(circle at 85% 90%, rgba(103,232,249,0.14), transparent 55%);
            background-size: 64px 64px, 64px 64px, 200% 200%, 200% 200%, 200% 200%, 200% 200%;
            animation: rsAurora 9s ease-in-out infinite;
        }
        @keyframes rsAurora {
            0%   { background-position: 0 0,     0 0,     0% 0%,   100% 20%, 20% 100%, 100% 100%; }
            50%  { background-position: 64px 64px, 64px 64px, 30% 20%, 70% 60%,  40% 70%, 70% 80%; }
            100% { background-position: 128px 128px, 128px 128px, 0% 0%,   100% 20%, 20% 100%, 100% 100%; }
        }

        /* faint drifting medical-icon watermarks */
        .rs-watermark {
            position: fixed; font-size: 7rem; opacity: 0.05;
            pointer-events: none; z-index: 0;
            color: #2dd4bf;
        }
        .rs-watermark-1 { top: 4%; left: 4%; animation: rsWmDrift 24s ease-in-out infinite; }
        .rs-watermark-2 { bottom: 6%; right: 6%; animation: rsWmDrift 28s ease-in-out infinite reverse; }
        .rs-watermark-3 { top: 55%; right: 3%; font-size: 5.5rem; animation: rsWmDrift 20s ease-in-out infinite 2s; }
        @keyframes rsWmDrift {
            0%, 100% { transform: translate(0, 0) rotate(-4deg); }
            50%      { transform: translate(18px, -24px) rotate(4deg); }
        }

        .rs-orb {
            position: absolute; border-radius: 50%; pointer-events: none; z-index: 0;
        }
        .rs-orb-1 {
            width: 8px; height: 8px; background: #2dd4bf;
            top: 18%; left: 8%;
            box-shadow: 0 0 40px 20px rgba(45,212,191,0.35);
            animation: rsFloat 4s ease-in-out infinite;
        }
        .rs-orb-2 {
            width: 6px; height: 6px; background: #38bdf8;
            top: 65%; right: 10%;
            box-shadow: 0 0 36px 18px rgba(56,189,248,0.3);
            animation: rsFloat 5s ease-in-out infinite 0.5s;
        }
        .rs-orb-3 {
            width: 10px; height: 10px; background: #34d399;
            bottom: 8%; left: 18%;
            box-shadow: 0 0 44px 22px rgba(52,211,153,0.3);
            animation: rsFloat 4.5s ease-in-out infinite 1s;
        }
        .rs-orb-4 {
            width: 7px; height: 7px; background: #67e8f9;
            top: 8%; right: 22%;
            box-shadow: 0 0 34px 16px rgba(103,232,249,0.25);
            animation: rsFloat 3.8s ease-in-out infinite 0.3s;
        }
        @keyframes rsFloat {
            0%, 100% { transform: translateY(0) translateX(0); }
            50%      { transform: translateY(-26px) translateX(14px); }
        }

        /* ECG / heartbeat trace — the medical signature visual */
        .rs-ecg-wrap {
            width: 100%; max-width: 460px; margin: 0.4rem auto 1.2rem auto;
            position: relative; z-index: 2; opacity: 0.9;
        }
        .rs-ecg-line {
            stroke: #2dd4bf; stroke-width: 2.4; fill: none;
            stroke-linecap: round; stroke-linejoin: round;
            stroke-dasharray: 340; stroke-dashoffset: 340;
            animation: rsEcgDraw 3.2s ease-in-out infinite;
            filter: drop-shadow(0 0 6px rgba(45,212,191,0.65));
        }
        @keyframes rsEcgDraw {
            0%   { stroke-dashoffset: 340; }
            55%  { stroke-dashoffset: 0; }
            100% { stroke-dashoffset: -340; }
        }
        .rs-ecg-dot {
            fill: #67e8f9;
            animation: rsEcgPulseDot 3.2s ease-in-out infinite;
        }
        @keyframes rsEcgPulseDot {
            0%, 100% { opacity: 0; }
            50%      { opacity: 1; }
        }

        .rs-brand-row {
            display: flex; align-items: center; justify-content: center; gap: 0.7rem;
            margin-bottom: 0.6rem; position: relative; z-index: 2;
            animation: rsFadeUp 0.6s ease both;
        }
        .rs-brand-badge {
            width: 50px; height: 50px; border-radius: 14px;
            background: linear-gradient(135deg, #2dd4bf, #0ea5e9);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 0 0 0 rgba(45, 212, 191, 0.55);
            animation: rsPulse 2.2s ease-out infinite;
        }
        @keyframes rsPulse {
            0%   { box-shadow: 0 0 0 0 rgba(45, 212, 191, 0.55); }
            70%  { box-shadow: 0 0 0 18px rgba(45, 212, 191, 0); }
            100% { box-shadow: 0 0 0 0 rgba(45, 212, 191, 0); }
        }
        .rs-badge-free {
            display: inline-flex; align-items: center; gap: 0.35rem;
            background: rgba(45,212,191,0.12); border: 1px solid rgba(45,212,191,0.35);
            color: #5eead4; font-family: 'Manrope', sans-serif; font-weight: 700;
            font-size: 0.72rem; padding: 0.3rem 0.8rem; border-radius: 999px;
            margin: 0 auto 0.9rem auto; width: fit-content;
            position: relative; z-index: 2;
            animation: rsFadeUp 0.6s ease both;
            text-shadow: 0 0 12px rgba(94, 234, 212, 0.7);
            box-shadow: 0 0 18px rgba(45,212,191,0.25);
        }
        .rs-brand-name {
            font-family: 'Sora', sans-serif; font-weight: 800;
            font-size: 1.8rem;
            background: linear-gradient(90deg, #ffffff, #99f6e4);
            -webkit-background-clip: text; background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 18px rgba(45,212,191,0.45), 0 0 34px rgba(14,165,233,0.25);
        }
        .rs-tagline {
            text-align: center; font-family: 'Manrope', sans-serif;
            color: #eef7f6; font-size: 1.1rem; font-weight: 500;
            margin-bottom: 1.6rem; position: relative; z-index: 2;
            animation: rsFadeUp 0.6s ease 0.1s both;
            text-shadow: 0 1px 8px rgba(0,0,0,0.4);
        }
        .rs-highlight,
        .rs-highlight-word {
            font-weight: 800;
            background: linear-gradient(90deg, #2dd4bf, #38bdf8, #34d399, #2dd4bf);
            background-size: 300% auto;
            -webkit-background-clip: text; background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rsWordIn 0.55s ease forwards, rsShine 4s linear infinite;
            text-shadow: 0 0 16px rgba(45,212,191,0.5);
        }
        @keyframes rsShine {
            0%   { background-position: 0% 50%; }
            100% { background-position: 300% 50%; }
        }
        .rs-wave {
            display: inline-block; animation: rsWave 2.2s ease-in-out infinite;
            transform-origin: 70% 70%;
        }
        @keyframes rsWave {
            0%, 100% { transform: rotate(0deg); }
            15%      { transform: rotate(14deg); }
            30%      { transform: rotate(-8deg); }
            45%      { transform: rotate(14deg); }
            60%      { transform: rotate(0deg); }
        }
        .rs-word {
            display: inline-block; opacity: 0;
            transform: translateY(8px);
            animation: rsWordIn 0.45s ease forwards;
        }
        @keyframes rsWordIn {
            to { opacity: 1; transform: translateY(0); }
        }

        /* feature cards — 2x2 grid */
        .rs-feature-grid {
            display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem;
            max-width: 480px; margin: 0 auto 1.6rem auto;
            position: relative; z-index: 2;
        }
        .rs-feature-card {
            background: rgba(255,255,255,0.05);
            border: 1.5px solid rgba(45,212,191,0.55);
            border-radius: 16px; padding: 0.85rem 0.9rem;
            display: flex; align-items: center; gap: 0.7rem;
            text-align: left;
            animation: rsFadeUp 0.6s ease both;
            transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
        }
        .rs-feature-card:hover {
            transform: translateY(-4px) scale(1.02);
            border-color: #2dd4bf;
            background: rgba(255,255,255,0.08);
        }
        .rs-feature-icon {
            width: 40px; height: 40px; min-width: 40px; border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.25rem;
            box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        }
        .rs-feature-icon.teal   { background: linear-gradient(135deg, #2dd4bf, #0f766e); }
        .rs-feature-icon.blue   { background: linear-gradient(135deg, #38bdf8, #0369a1); }
        .rs-feature-icon.green  { background: linear-gradient(135deg, #34d399, #047857); }
        .rs-feature-icon.amber  { background: linear-gradient(135deg, #fbbf24, #b45309); }
        .rs-feature-text b {
            display: block; color: #f5f5ff; font-family: 'Manrope', sans-serif;
            font-size: 0.85rem; font-weight: 700; margin-bottom: 0.1rem;
            text-shadow: 0 0 10px rgba(45,212,191,0.35);
        }
        .rs-feature-text span {
            display: block; color: #e8f4f3;
            font-family: 'Manrope', sans-serif; font-size: 0.72rem; line-height: 1.3;
        }
        .rs-feature-card:nth-child(1) { animation-delay: 0.15s; }
        .rs-feature-card:nth-child(2) { animation-delay: 0.25s; }
        .rs-feature-card:nth-child(3) { animation-delay: 0.35s; }
        .rs-feature-card:nth-child(4) { animation-delay: 0.45s; }
        @media (max-width: 560px) {
            .rs-feature-grid { grid-template-columns: 1fr; }
        }

        @keyframes rsFadeUp {
            from { opacity: 0; transform: translateY(12px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* glass card with a bold pulsing border */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(20, 48, 54, 0.55) !important;
            border-radius: 22px !important;
            border: 2.5px solid #2dd4bf !important;
            padding: 0.6rem 0.6rem 1.2rem 0.6rem !important;
            position: relative; z-index: 2;
            box-shadow: 0 25px 70px rgba(0,0,0,0.55), 0 0 30px rgba(45,212,191,0.35) !important;
            animation: rsFadeUp 0.7s ease 0.2s both, rsBorderGlow 3s ease-in-out infinite;
        }
        @keyframes rsBorderGlow {
            0%, 100% { border-color: #2dd4bf; box-shadow: 0 25px 70px rgba(0,0,0,0.55), 0 0 26px rgba(45,212,191,0.3); }
            50%      { border-color: #38bdf8; box-shadow: 0 25px 70px rgba(0,0,0,0.55), 0 0 40px rgba(56,189,248,0.55); }
        }

        .rs-card-badge {
            width: 56px; height: 56px; border-radius: 16px;
            background: linear-gradient(135deg, #2dd4bf, #0ea5e9);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.7rem;
            margin: -2.4rem auto 0.7rem auto;
            box-shadow: 0 10px 28px rgba(14,165,233,0.5), 0 0 0 5px #08161c;
            position: relative; z-index: 3;
            animation: rsFadeUp 0.6s ease both, rsPulse 2.4s ease-out infinite 0.6s;
        }

        .rs-trust-row {
            display: flex; align-items: center; justify-content: center; gap: 1rem;
            margin: 0.9rem 0 0.2rem 0; flex-wrap: wrap;
        }
        .rs-trust-item {
            display: flex; align-items: center; gap: 0.35rem;
            font-family: 'Manrope', sans-serif; font-size: 0.72rem; font-weight: 600;
            color: #e8f4f3;
        }
        .rs-trust-item b { color: #5eead4; }

        h3.rs-card-title {
            font-family: 'Sora', sans-serif;
            font-size: 1.4rem; font-weight: 800;
            text-align: center; margin: 0.6rem 0 0.2rem 0;
            background: linear-gradient(90deg, #ffffff, #99f6e4, #ffffff);
            background-size: 220% auto;
            -webkit-background-clip: text; background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rsShine 5s linear infinite;
            text-shadow: 0 0 20px rgba(45,212,191,0.4);
        }
        p.rs-card-sub {
            font-family: 'Manrope', sans-serif; color: #e8f4f3;
            font-size: 0.85rem; text-align: center; margin-bottom: 1.1rem;
        }

        .st-key-google_btn button {
            background: #ffffff !important;
            color: #1f2430 !important;
            border: none !important;
            border-radius: 12px !important;
            font-family: 'Manrope', sans-serif !important;
            font-weight: 700 !important;
            height: 3rem !important;
            box-shadow: 0 6px 16px rgba(0,0,0,0.3), 0 0 22px rgba(45,212,191,0.25);
            transition: transform 0.15s ease;
            position: relative; overflow: hidden;
        }
        .st-key-google_btn button:hover { transform: translateY(-2px) scale(1.01); }
        .st-key-google_btn button::after {
            content: "";
            position: absolute; top: 0; left: -60%;
            width: 40%; height: 100%;
            background: linear-gradient(120deg, transparent, rgba(14,165,233,0.35), transparent);
            transform: skewX(-20deg);
            animation: rsShimmer 3.2s ease-in-out infinite;
        }
        @keyframes rsShimmer {
            0%   { left: -60%; }
            50%  { left: 130%; }
            100% { left: 130%; }
        }

        .rs-divider {
            display: flex; align-items: center; gap: 0.7rem;
            font-family: 'Manrope', sans-serif; font-weight: 700;
            font-size: 0.76rem; margin: 1.1rem 0.3rem;
            background: linear-gradient(90deg, #2dd4bf, #38bdf8, #34d399, #2dd4bf);
            background-size: 300% auto;
            -webkit-background-clip: text; background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rsShine 4s linear infinite;
        }
        .rs-divider::before, .rs-divider::after {
            content: ""; flex: 1; height: 1px;
            background: rgba(45,212,191,0.3);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.3rem !important; border-bottom: none !important;
            background: rgba(255,255,255,0.05) !important;
            border: 1.5px solid rgba(45,212,191,0.55) !important;
            border-radius: 12px !important;
            padding: 0.3rem !important;
            width: fit-content !important;
            overflow: hidden !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Manrope', sans-serif; font-weight: 700;
            color: #e8f4f3;
            border-radius: 9px !important;
            padding: 0.4rem 1.1rem !important;
            margin: 0 !important;
            transition: color 0.2s ease, background 0.2s ease;
            background: transparent !important;
            overflow: hidden !important;
        }
        .stTabs [aria-selected="true"] {
            color: #04141a !important;
            background: linear-gradient(90deg, #2dd4bf, #0ea5e9) !important;
            border-radius: 9px !important;
        }
        .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
        .stTabs [data-baseweb="tab-border"] { display: none !important; }
        .stTabs [data-baseweb="tab-panel"] { padding-top: 0.6rem !important; }

        .stTextInput label {
            font-family: 'Manrope', sans-serif !important;
            color: rgba(226,226,245,0.85) !important; font-weight: 600 !important;
            font-size: 0.85rem !important;
        }
        .stTextInput input {
            background: rgba(255,255,255,0.05) !important;
            border: 1.5px solid rgba(45,212,191,0.6) !important;
            color: #f5f5ff !important;
            border-radius: 10px !important;
        }
        .stTextInput input:focus {
            border: 1px solid #2dd4bf !important;
            box-shadow: 0 0 0 3px rgba(45,212,191,0.25) !important;
        }
        .stTextInput input::placeholder { color: rgba(226,226,245,0.32) !important; }
        [data-testid="stIconMaterial"] { font-size: 0 !important; }
        [data-testid="stIconMaterial"]::after { content: "\\1F441"; font-size: 1rem; color: rgba(226,226,245,0.7); }

        /* primary submit buttons — cover both old and new streamlit button DOM shapes */
        .stButton button,
        button[kind="primary"],
        button[kind="formSubmit"],
        [data-testid="stFormSubmitButton"] button,
        [data-testid="stBaseButton-primary"],
        [data-testid="stBaseButton-secondaryFormSubmit"] {
            background: linear-gradient(135deg, #2dd4bf, #0ea5e9) !important;
            background-size: 200% 200% !important;
            animation: rsGradShift 5s ease infinite !important;
            color: #0a0e1e !important;
            border: none !important;
            border-radius: 12px !important;
            font-family: 'Manrope', sans-serif !important;
            font-weight: 800 !important;
            height: 3rem !important;
            box-shadow: 0 8px 28px rgba(45,212,191,0.45), 0 0 24px rgba(14,165,233,0.35) !important;
            transition: transform 0.15s ease, box-shadow 0.2s ease !important;
        }
        .stButton button:hover,
        [data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 32px rgba(45,212,191,0.6), 0 0 34px rgba(14,165,233,0.5) !important;
        }
        @keyframes rsGradShift {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stAlert { border-radius: 12px !important; }
        </style>

        <div class="rs-orb rs-orb-1"></div>
        <div class="rs-orb rs-orb-2"></div>
        <div class="rs-orb rs-orb-3"></div>
        <div class="rs-orb rs-orb-4"></div>

        <div class="rs-watermark rs-watermark-1">🩺</div>
        <div class="rs-watermark rs-watermark-2">➕</div>
        <div class="rs-watermark rs-watermark-3">💊</div>
        """,
        unsafe_allow_html=True,
    )


def require_login():
    if st.user.is_logged_in:
        # Google sign-in only gives us st.user — make sure there's a matching
        # row in our own users table, and store it the same way the email/
        # password flow does, so the rest of the app can just read
        # st.session_state["user"] regardless of how someone signed in.
        if "user" not in st.session_state or st.session_state["user"].get("email") != st.user.email:
            st.session_state["user"] = find_or_create_google_user(st.user.email, st.user.name)
        return True

    _login_css()

    # Build the tagline as individually-animated words so it "types itself in"
    tagline_parts = [
        ("From", False), ("confusing", False), ("lab", False), ("values", False),
        ("to", False),
        ("clear", True), ("answers", True), ("—", False),
        ("ReportSathi", False), ("explains", False), ("your", False), ("report", False),
        ("the", False), ("way", False), ("a", False), ("doctor", False), ("would,", False),
        ("if", False), ("they", False), ("had", False), ("the", False), ("time,", False),
        ("in", False), ("English,", False), ("Hindi", False), ("or", False), ("Bengali.", False),
    ]
    words_html = []
    for i, (word, highlight) in enumerate(tagline_parts):
        delay = round(0.25 + i * 0.045, 3)
        cls = "rs-word rs-highlight-word" if highlight else "rs-word"
        words_html.append(
            f'<span class="{cls}" style="animation-delay:{delay}s">{word}</span>'
        )
    tagline_html = " ".join(words_html)

    st.markdown(
        f"""
        <div class="rs-brand-row">
            <div class="rs-brand-badge">🩺</div>
            <div class="rs-brand-name">ReportSathi</div>
        </div>
        <p class="rs-tagline">{tagline_html}</p>

        <div class="rs-ecg-wrap">
            <svg viewBox="0 0 460 60" width="100%" height="60" preserveAspectRatio="none">
                <path class="rs-ecg-line" d="M0,30 L90,30 L110,30 L120,8 L135,52 L150,18 L165,30 L200,30
                    L260,30 L280,30 L290,8 L305,52 L320,18 L335,30 L400,30 L460,30" />
                <circle class="rs-ecg-dot" cx="120" cy="8" r="3.5" />
                <circle class="rs-ecg-dot" cx="290" cy="8" r="3.5" />
            </svg>
        </div>

        <div class="rs-badge-free">✨ Free to use — no card required</div>

        <div class="rs-feature-grid">
            <div class="rs-feature-card">
                <div class="rs-feature-icon teal">🗣️</div>
                <div class="rs-feature-text"><b>Voice Q&amp;A</b><span>ask a question by voice and hear the answer read back</span></div>
            </div>
            <div class="rs-feature-card">
                <div class="rs-feature-icon blue">📈</div>
                <div class="rs-feature-text"><b>Health Timeline</b><span>tracks your values across reports and flags early drift</span></div>
            </div>
            <div class="rs-feature-card">
                <div class="rs-feature-icon green">📄</div>
                <div class="rs-feature-text"><b>Doctor-visit summary</b><span>a one-page PDF to carry to your appointment</span></div>
            </div>
            <div class="rs-feature-card">
                <div class="rs-feature-icon amber">🔒</div>
                <div class="rs-feature-text"><b>Grounded answers</b><span>responses are based only on your own report</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([0.5, 5, 0.5])
    with mid:
        with st.container(border=True):
            st.markdown('<div class="rs-card-badge">🩺</div>', unsafe_allow_html=True)
            st.markdown('<h3 class="rs-card-title">Welcome to ReportSathi</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="rs-card-sub">Sign in with Google, or continue with your email</p>',
                unsafe_allow_html=True,
            )

            if st.button("Continue with Google", key="google_btn", use_container_width=True):
                st.login("google")

            st.markdown(
                """
                <div class="rs-trust-row">
                    <div class="rs-trust-item">🔒 <b>Private &amp; secure</b></div>
                    <div class="rs-trust-item">⚡ <b>Ready in seconds</b></div>
                    <div class="rs-trust-item">📩 <b>No spam, ever</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown('<div class="rs-divider">or continue with email</div>', unsafe_allow_html=True)

            tab_login, tab_signup = st.tabs(["Log in", "Create account"])

            with tab_login:
                with st.form("login_form", clear_on_submit=False):
                    email = st.text_input("📧 Email", key="login_email", placeholder="you@example.com")
                    password = st.text_input(
                        "🔒 Password", type="password", key="login_password", placeholder="••••••••"
                    )
                    submitted = st.form_submit_button(
                        "Log in", type="primary", use_container_width=True
                    )
                    if submitted:
                        user = login(email, password)
                        if user:
                            st.session_state["user"] = user
                            st.rerun()
                        else:
                            st.error("Incorrect email or password. Please try again.")

            with tab_signup:
                with st.form("signup_form", clear_on_submit=False):
                    name = st.text_input("🧑 Name", key="signup_name", placeholder="Your name")
                    email_s = st.text_input(
                        "📧 Email", key="signup_email", placeholder="you@example.com"
                    )
                    password_s = st.text_input(
                        "🔒 Password",
                        type="password",
                        key="signup_password",
                        placeholder="At least 6 characters",
                    )
                    submitted_s = st.form_submit_button(
                        "Create account", type="primary", use_container_width=True
                    )
                    if submitted_s:
                        ok, msg = signup(name, email_s, password_s)
                        if ok:
                            st.success("Account created successfully. Please log in from the tab above.")
                        else:
                            st.error(msg)

    return False


def _sidebar_user_card(name: str, email: str):
    initial = (name or email or "?").strip()[:1].upper()
    st.markdown(
        f"""
        <div class="rs-side-brand">
            <div class="rs-side-brand-badge">🩺</div>
            <div class="rs-side-brand-name">ReportSathi</div>
        </div>
        <div class="rs-user-card">
            <div class="rs-avatar-row">
                <div class="rs-avatar">{initial}</div>
                <div>
                    <div class="rs-user-name">{name}</div>
                    <div class="rs-user-email">{email}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def logout_button():
    with st.sidebar:
        user = getattr(st, "user", None)
        if user is not None and getattr(user, "is_logged_in", False):
            name = getattr(user, "name", None) or getattr(user, "email", "Account")
            email = getattr(user, "email", "")
            _sidebar_user_card(name, email)
            if st.button("🚪 Log out", use_container_width=True):
                if "user" in st.session_state:
                    del st.session_state["user"]
                st.logout()
        elif "user" in st.session_state:
            user_row = st.session_state["user"]
            _sidebar_user_card(user_row.get("name", "Account"), user_row.get("email", ""))
            if st.button("🚪 Log out", use_container_width=True):
                del st.session_state["user"]
                st.rerun()