"""Shared visual system for AI&DS Career Compass 3.0."""
import streamlit as st


def apply_theme(active_page="Career Compass"):
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root { --ink:#20234a; --muted:#6d7188; --purple:#6259d8; --teal:#1aa890; --coral:#ff8b72; --cream:#fbfaf7; --line:#e9e7f4; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:radial-gradient(circle at 94% 2%,rgba(218,246,239,.45),transparent 23%),linear-gradient(180deg,#fbfaf7 0%,#f7f7ff 65%,#fbfaf7 100%); color:var(--ink); }
    [data-testid="stHeader"] { background:rgba(251,250,247,.88); }
    .block-container { max-width:1210px; padding-top:1.35rem; padding-bottom:3.5rem; }
    h1,h2,h3,h4 { font-family:'Manrope','DM Sans',sans-serif !important; color:var(--ink); letter-spacing:-.035em; }
    h1 { font-weight:800 !important; line-height:1.08 !important; }
    h2,h3,h4 { font-weight:750 !important; }
    p, label, .stMarkdown { color:var(--ink); }
    a { color:#5149bb !important; font-weight:600; }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#26264f 0%,#42409b 65%,#2e777b 125%); }
    [data-testid="stSidebar"] * { color:#f7f6ff !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#e1e0fb !important; }
    [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.18); }
    [data-testid="stSidebar"] a { text-decoration:none; }
    .cc-hero { position:relative; overflow:hidden; padding:2.35rem 2.5rem; border-radius:29px; background:radial-gradient(circle at 89% 15%,rgba(255,255,255,.24),transparent 24%),radial-gradient(circle at 75% 110%,rgba(255,139,114,.24),transparent 32%),linear-gradient(125deg,#282750 0%,#514bb6 53%,#1c9f96 120%); color:#fff; margin:.2rem 0 1.35rem; box-shadow:0 18px 45px rgba(66,61,157,.18); }
    .cc-hero:after { content:'✦'; position:absolute; right:5%; bottom:-38px; font-size:10rem; line-height:1; color:rgba(255,255,255,.08); transform:rotate(-14deg); pointer-events:none; }
    .cc-hero h1 { color:#fff !important; font-size:clamp(2.05rem,4vw,3.25rem); margin:0; position:relative; z-index:1; }
    .cc-hero p { color:#eeedff !important; font-size:1.04rem; line-height:1.6; margin:.82rem 0 0; max-width:760px; position:relative; z-index:1; }
    .cc-eyebrow { text-transform:uppercase; letter-spacing:.15em; font-size:.74rem; font-weight:800; color:#bff8ed; margin-bottom:.7rem; position:relative; z-index:1; }
    .cc-chip { display:inline-block; border:1px solid rgba(255,255,255,.3); background:rgba(255,255,255,.08); border-radius:999px; padding:.37rem .72rem; color:#fff; font-size:.79rem; margin:.95rem .35rem 0 0; position:relative; z-index:1; }
    .cc-hero-market { background:radial-gradient(circle at 88% 10%,rgba(255,255,255,.24),transparent 23%),linear-gradient(125deg,#282750 0%,#4f4aa9 52%,#237fa2 125%); }
    .cc-hero-learning { background:radial-gradient(circle at 85% 7%,rgba(255,255,255,.24),transparent 24%),linear-gradient(125deg,#2a2854 0%,#6455cb 48%,#18a58e 125%); }
    .cc-section { padding:.3rem 0 .2rem; }
    [data-testid="stMetric"] { background:rgba(255,255,255,.92); border:1px solid #eeedf8; border-radius:17px; padding:.92rem 1rem; box-shadow:0 6px 20px rgba(39,39,88,.045); }
    [data-testid="stMetricLabel"] { color:var(--muted) !important; }
    [data-testid="stMetricValue"] { color:var(--ink) !important; font-family:'Manrope',sans-serif; }
    [data-testid="stMetricDelta"] { font-size:.78rem; }
    [data-testid="stVerticalBlockBorderWrapper"] { border-color:var(--line) !important; border-radius:20px !important; background:rgba(255,255,255,.9); box-shadow:0 8px 24px rgba(39,39,88,.04); }
    [data-testid="stForm"] { border:1px solid var(--line); border-radius:22px; padding:1.35rem; background:rgba(255,255,255,.93); box-shadow:0 10px 30px rgba(39,39,88,.045); }
    .stButton > button, .stFormSubmitButton > button, [data-testid="stPageLink"] a { border-radius:12px; font-weight:700; min-height:2.75rem; transition:transform .15s ease,box-shadow .15s ease; }
    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background:linear-gradient(110deg,#635bdb,#4d49bc); color:#fff; border:0; box-shadow:0 8px 18px rgba(99,91,219,.22); }
    .stButton > button:hover, .stFormSubmitButton > button:hover { transform:translateY(-1px); box-shadow:0 10px 22px rgba(39,39,88,.12); }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, textarea { border-radius:12px !important; border-color:#dfdef0 !important; background:#fff !important; }
    [data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#635bdb,#20b8a6); border-radius:999px; }
    [data-testid="stAlert"] { border-radius:14px; }
    [data-testid="stExpander"] { border-color:var(--line); border-radius:15px; background:rgba(255,255,255,.7); }
    .cc-note { color:#777b95; font-size:.88rem; }
    .cc-step-number { display:flex; align-items:center; justify-content:center; width:44px; height:44px; border-radius:14px; background:linear-gradient(135deg,#eeeaff,#dff8ef); color:#5149bb; font-family:'Manrope',sans-serif; font-weight:800; font-size:1.1rem; }
    .cc-footer { text-align:center; padding:1.2rem .2rem .3rem; color:#8b8ea5; font-size:.8rem; }
    @media (max-width: 700px) { .cc-hero { padding:1.55rem; border-radius:22px; } .block-container { padding-top:1rem; } .cc-hero:after { right:0; font-size:6rem; } }
    </style>
    """, unsafe_allow_html=True)
