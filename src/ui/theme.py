"""Global White + Navy Blue premium theme for the Streamlit UI.

This module holds one big CSS string that is injected once via
`st.markdown(BASE_CSS, unsafe_allow_html=True)`. It:
  - restyles Streamlit's own widgets (buttons, file uploader, metrics,
    expanders, spinner) via their stable `data-testid` hooks
  - defines the custom classes used by the hand-written HTML blocks in
    app.py (sticky header, hero, feature chips, footer, empty state)
  - defines reusable animation keyframes (fade-in-up, chip-pop, float)
  - respects `prefers-reduced-motion` by disabling all animation/transition
No functionality lives here -- this file is presentation only.
"""

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --navy-deep: #0B1F3A;
  --navy: #12355B;
  --navy-soft: #1F4E86;
  --bg: #FFFFFF;
  --bg-light: #F5F8FC;
  --text: #0B1F3A;
  --text-muted: #55708D;
  --border: #E3EBF5;
  --shadow-sm: 0 2px 10px rgba(11, 31, 58, 0.06);
  --shadow-md: 0 10px 30px rgba(11, 31, 58, 0.10);
  --shadow-lg: 0 20px 50px rgba(11, 31, 58, 0.16);
  --radius: 16px;
}

html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  color: var(--text);
}

.stApp {
  background: linear-gradient(180deg, var(--bg-light) 0%, var(--bg) 320px);
}

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { padding-top: 1rem !important; max-width: 1180px; }

/* ---------- Keyframes ---------- */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes chipPop {
  from { opacity: 0; transform: translateY(10px) scale(.92); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes floatY {
  0%, 100% { transform: translateY(0px); }
  50%      { transform: translateY(-10px); }
}
@keyframes shimmer {
  0%   { background-position: -300px 0; }
  100% { background-position: 300px 0; }
}

/* ---------- Sticky top bar ---------- */
.hr-topbar {
  position: sticky; top: 0; z-index: 999;
  backdrop-filter: blur(10px);
  background: rgba(255,255,255,0.82);
  border-bottom: 1px solid var(--border);
  margin: -1rem -1rem 0 -1rem;
  padding: 0 1rem;
}
.hr-topbar-inner {
  max-width: 1180px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 0;
}
.hr-logo {
  font-weight: 800; font-size: 1.15rem; letter-spacing: .3px;
  color: var(--navy-deep);
}
.hr-logo span { color: var(--navy-soft); }
.hr-topbar-badge {
  font-size: .78rem; font-weight: 600; color: var(--navy);
  background: var(--bg-light); border: 1px solid var(--border);
  padding: 6px 14px; border-radius: 999px;
}

/* ---------- Hero ---------- */
.hr-hero {
  text-align: center; padding: 56px 12px 28px 12px;
  animation: fadeInUp .7s ease both;
}
.hr-hero-badge {
  display: inline-block; font-size: .78rem; font-weight: 700;
  color: var(--navy-soft); background: var(--bg-light);
  border: 1px solid var(--border); padding: 6px 16px; border-radius: 999px;
  margin-bottom: 18px; animation: floatY 4.5s ease-in-out infinite;
}
.hr-hero-title {
  font-size: clamp(2rem, 5vw, 3.1rem); font-weight: 800; line-height: 1.15;
  color: var(--navy-deep); margin: 0 0 16px 0;
}
.hr-hero-title span {
  background: linear-gradient(120deg, var(--navy) 0%, var(--navy-soft) 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hr-hero-sub {
  max-width: 680px; margin: 0 auto; color: var(--text-muted);
  font-size: 1.05rem; line-height: 1.6;
}
.hr-chip-row {
  display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
  margin-top: 26px;
}
.hr-chip {
  background: #fff; border: 1px solid var(--border); box-shadow: var(--shadow-sm);
  padding: 10px 16px; border-radius: 999px; font-size: .88rem; font-weight: 600;
  color: var(--navy); animation: chipPop .55s ease both;
  transition: transform .25s ease, box-shadow .25s ease;
}
.hr-chip:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }

.hr-section-label {
  font-size: .8rem; font-weight: 700; letter-spacing: 1.4px; text-transform: uppercase;
  color: var(--navy-soft); margin: 8px 0 10px 2px;
}

.hr-card-label {
  font-weight: 700; color: var(--navy-deep); margin-bottom: 6px; font-size: .95rem;
}

.hr-empty-state {
  text-align: center; color: var(--text-muted); background: var(--bg-light);
  border: 1px dashed var(--border); border-radius: var(--radius);
  padding: 34px 18px; margin-top: 18px; animation: fadeInUp .5s ease both;
}

/* ---------- Streamlit widget restyling ---------- */
div[data-testid="stFileUploaderDropzone"] {
  background: #fff !important; border: 1.5px dashed var(--border) !important;
  border-radius: var(--radius) !important; transition: border-color .25s ease, box-shadow .25s ease;
}
div[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--navy-soft) !important; box-shadow: var(--shadow-sm);
}

button[kind="primary"], .stButton > button {
  background: linear-gradient(135deg, var(--navy) 0%, var(--navy-soft) 100%) !important;
  color: #fff !important; border: none !important; border-radius: 999px !important;
  padding: 0.6rem 1.6rem !important; font-weight: 700 !important;
  box-shadow: var(--shadow-sm); transition: transform .2s ease, box-shadow .2s ease;
}
.stButton > button:hover:enabled {
  transform: translateY(-2px); box-shadow: var(--shadow-md);
}
.stButton > button:disabled { opacity: .45; }

div[data-testid="stExpander"] {
  border: 1px solid var(--border) !important; border-radius: var(--radius) !important;
  box-shadow: var(--shadow-sm); overflow: hidden;
}
div[data-testid="stExpander"] summary { font-weight: 600; color: var(--navy-deep); }

div[data-testid="stMetric"] {
  background: #fff; border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px 18px; box-shadow: var(--shadow-sm);
}

.stSpinner > div { border-top-color: var(--navy) !important; }

/* ---------- Footer ---------- */
.hr-footer {
  margin: 60px -1rem -1rem -1rem; padding: 28px 1rem;
  background: linear-gradient(135deg, var(--navy-deep), var(--navy));
  color: #E8EEF7;
}
.hr-footer-inner {
  max-width: 1180px; margin: 0 auto; display: flex; align-items: center;
  justify-content: space-between; flex-wrap: wrap; gap: 10px;
}
.hr-footer .hr-logo { color: #fff; }
.hr-footer .hr-logo span { color: #9FC1EE; }
.hr-footer-links { display: flex; gap: 10px; font-size: .85rem; color: #C7D6EA; }
.hr-footer-copy { font-size: .8rem; color: #9FB4D6; }

/* ---------- Reduced motion ---------- */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.001ms !important; animation-iteration-count: 1 !important;
      transition-duration: 0.001ms !important; scroll-behavior: auto !important; }
}
</style>
"""
