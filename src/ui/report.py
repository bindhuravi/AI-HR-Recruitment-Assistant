"""Builds the animated, White + Navy Blue results report shown after a
candidate is screened. Rendered via `st.components.v1.html(...)`, which
(unlike `st.markdown`) actually executes <script> tags -- so this is where
the real interactive touches live: animated count-up score numbers,
scroll-reveal on the question cards, and CSS scaleX() bar-fill animations.

All candidate/job-description text originates from an LLM's parsing of a
resume/JD, so everything is HTML-escaped before being interpolated into
the template to avoid breaking the markup.
"""
import html
import json
from typing import Any, Dict, List


def _esc(value: Any) -> str:
    return html.escape(str(value)) if value not in (None, "") else ""


def _chips(items: List[str], css_class: str) -> str:
    if not items:
        return '<span class="muted">None</span>'
    parts = []
    for i, s in enumerate(items):
        parts.append(
            f'<span class="chip {css_class}" style="animation-delay:{0.03 * i:.2f}s">{_esc(s)}</span>'
        )
    return "".join(parts)


def _questions(items: List[str], icon: str) -> str:
    if not items:
        return '<p class="muted">No questions generated.</p>'
    rows = []
    for i, q in enumerate(items):
        rows.append(
            f'<div class="q-card reveal" style="transition-delay:{0.06 * i:.2f}s">'
            f'<span class="q-icon">{icon}</span><span>{_esc(q)}</span></div>'
        )
    return "".join(rows)


def build_report_html(
    candidate: Dict[str, Any],
    jd: Dict[str, Any],
    match: Dict[str, Any],
    questions: Dict[str, Any],
) -> str:
    overall = round(float(match.get("overall_score", 0) or 0), 1)
    skill_score = round(float(match.get("skill_match_score", 0) or 0), 1)
    exp_score = round(float(match.get("experience_match_score", 0) or 0), 1)

    candidate_name = _esc(candidate.get("name") or "This candidate")
    role_title = _esc(jd.get("title") or "the role")
    company = _esc(jd.get("company") or "")

    matched_html = _chips(match.get("matched_skills", []), "chip-matched")
    missing_html = _chips(match.get("missing_skills", []), "chip-missing")
    rationale_html = _esc(match.get("rationale", ""))

    tech_html = _questions(questions.get("technical_questions", []), "&#128295;")
    beh_html = _questions(questions.get("behavioral_questions", []), "&#129309;")
    gap_html = _questions(questions.get("gap_probing_questions", []), "&#128269;")

    band_label, band_class = _score_band(overall)

    # Numeric targets passed to the JS count-up / bar-fill animation.
    score_targets = json.dumps({"overall": overall, "skill": skill_score, "exp": exp_score})

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
{_REPORT_CSS}
</style>
</head>
<body>
  <div class="wrap">

    <div class="summary-row">
      <div class="score-card reveal">
        <div class="score-ring" id="ring-overall">
          <span class="score-num" id="num-overall">0</span><span class="score-pct">%</span>
        </div>
        <div class="score-label">Overall Match</div>
        <div class="badge {band_class}">{band_label}</div>
      </div>

      <div class="bars-card reveal" style="transition-delay:.08s">
        <div class="bar-block">
          <div class="bar-head"><span>Skill Match</span><span id="num-skill">0%</span></div>
          <div class="bar-track"><div class="bar-fill fill-skill" id="bar-skill"></div></div>
        </div>
        <div class="bar-block">
          <div class="bar-head"><span>Experience Match</span><span id="num-exp">0%</span></div>
          <div class="bar-track"><div class="bar-fill fill-exp" id="bar-exp"></div></div>
        </div>
        <p class="rationale">{rationale_html}</p>
      </div>
    </div>

    <div class="skills-row">
      <div class="skills-card reveal" style="transition-delay:.12s">
        <h3><span class="dot dot-good"></span>Matched Skills</h3>
        <div class="chip-wrap">{matched_html}</div>
      </div>
      <div class="skills-card reveal" style="transition-delay:.18s">
        <h3><span class="dot dot-gap"></span>Skill Gaps</h3>
        <div class="chip-wrap">{missing_html}</div>
      </div>
    </div>

    <h3 class="section-title reveal" style="transition-delay:.22s">Suggested Interview Questions</h3>
    <p class="section-sub reveal" style="transition-delay:.24s">
      For {candidate_name} &rarr; {role_title}{(' at ' + company) if company else ''}
    </p>

    <div class="q-columns">
      <div class="q-col">
        <h4>Technical</h4>
        {tech_html}
      </div>
      <div class="q-col">
        <h4>Behavioral</h4>
        {beh_html}
      </div>
      <div class="q-col">
        <h4>Gap-Probing</h4>
        {gap_html}
      </div>
    </div>

  </div>

<script>
  const targets = {score_targets};

  function countUp(el, target, suffix, duration) {{
    const start = performance.now();
    function step(now) {{
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (t < 1) requestAnimationFrame(step);
    }}
    requestAnimationFrame(step);
  }}

  function fillBar(el, pct) {{
    el.style.setProperty('--target', pct + '%');
    requestAnimationFrame(() => {{ el.style.width = pct + '%'; }});
  }}

  window.addEventListener('DOMContentLoaded', () => {{
    document.getElementById('num-overall').textContent = '0';
    countUp(document.getElementById('num-overall'), targets.overall, '', 1100);
    countUp(document.getElementById('num-skill'), targets.skill, '%', 900);
    countUp(document.getElementById('num-exp'), targets.exp, '%', 900);
    fillBar(document.getElementById('bar-skill'), targets.skill);
    fillBar(document.getElementById('bar-exp'), targets.exp);

    const revealEls = document.querySelectorAll('.reveal');
    const io = new IntersectionObserver((entries) => {{
      entries.forEach((entry) => {{
        if (entry.isIntersecting) {{
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }}
      }});
    }}, {{ threshold: 0.12 }});
    revealEls.forEach((el) => io.observe(el));
  }});
</script>
</body>
</html>"""


def _score_band(score: float):
    if score >= 80:
        return "Strong Fit", "badge-strong"
    if score >= 55:
        return "Possible Fit", "badge-mid"
    return "Needs Review", "badge-low"


_REPORT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --navy-deep: #0B1F3A;
  --navy: #12355B;
  --navy-soft: #1F4E86;
  --bg-light: #F5F8FC;
  --text: #0B1F3A;
  --text-muted: #55708D;
  --border: #E3EBF5;
  --good: #1F8A5C;
  --gap: #B5502E;
  --shadow-sm: 0 2px 10px rgba(11,31,58,.06);
  --shadow-md: 0 12px 30px rgba(11,31,58,.12);
  --radius: 16px;
}
* { box-sizing: border-box; }
body {
  margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: var(--text); background: transparent;
}
.wrap { padding: 6px 2px 30px 2px; }
.muted { color: var(--text-muted); font-size: .9rem; }

.reveal { opacity: 0; transform: translateY(16px); transition: opacity .55s ease, transform .55s ease; }
.reveal.in-view { opacity: 1; transform: translateY(0); }

.summary-row { display: flex; gap: 18px; flex-wrap: wrap; margin-bottom: 18px; }
.score-card, .bars-card, .skills-card {
  background: #fff; border: 1px solid var(--border); border-radius: var(--radius);
  box-shadow: var(--shadow-sm); padding: 22px;
}
.score-card {
  flex: 0 0 220px; display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center; gap: 10px;
}
.score-ring {
  width: 140px; height: 140px; border-radius: 50%;
  background: conic-gradient(var(--navy-soft) 0deg, var(--navy) 360deg);
  display: flex; align-items: center; justify-content: center; position: relative;
  box-shadow: var(--shadow-md);
}
.score-ring::before {
  content: ""; position: absolute; inset: 10px; border-radius: 50%; background: #fff;
}
.score-num { position: relative; font-size: 2.1rem; font-weight: 800; color: var(--navy-deep); }
.score-pct { position: relative; font-size: 1.1rem; font-weight: 700; color: var(--navy-soft); margin-left: 2px; }
.score-label { font-weight: 700; color: var(--navy-deep); font-size: .95rem; }
.badge { font-size: .75rem; font-weight: 700; padding: 5px 14px; border-radius: 999px; }
.badge-strong { background: #E7F5EE; color: var(--good); }
.badge-mid { background: #FFF3E4; color: #A2601A; }
.badge-low { background: #FBEAE5; color: var(--gap); }

.bars-card { flex: 1 1 320px; display: flex; flex-direction: column; gap: 16px; }
.bar-head { display: flex; justify-content: space-between; font-weight: 600; font-size: .88rem; color: var(--navy-deep); margin-bottom: 6px; }
.bar-track { height: 10px; border-radius: 999px; background: var(--bg-light); overflow: hidden; }
.bar-fill { height: 100%; width: 0%; border-radius: 999px; transition: width 1.1s cubic-bezier(.22,1,.36,1); }
.fill-skill { background: linear-gradient(90deg, var(--navy), var(--navy-soft)); }
.fill-exp { background: linear-gradient(90deg, #2E6BA6, #5B9BD5); }
.rationale { color: var(--text-muted); font-size: .92rem; line-height: 1.55; margin: 4px 0 0 0; }

.skills-row { display: flex; gap: 18px; flex-wrap: wrap; margin-bottom: 26px; }
.skills-card { flex: 1 1 300px; }
.skills-card h3 { margin: 0 0 14px 0; font-size: .95rem; color: var(--navy-deep); display: flex; align-items: center; gap: 8px; }
.dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.dot-good { background: var(--good); }
.dot-gap { background: var(--gap); }
.chip-wrap { display: flex; flex-wrap: wrap; gap: 8px; }
.chip {
  font-size: .8rem; font-weight: 600; padding: 6px 13px; border-radius: 999px;
  animation: chipPop .5s ease both; transition: transform .2s ease;
}
.chip:hover { transform: translateY(-2px); }
.chip-matched { background: #E7F5EE; color: var(--good); }
.chip-missing { background: #FBEAE5; color: var(--gap); }
@keyframes chipPop { from { opacity:0; transform: translateY(8px) scale(.94);} to { opacity:1; transform: translateY(0) scale(1);} }

.section-title { font-size: 1.15rem; font-weight: 800; color: var(--navy-deep); margin: 6px 0 2px 0; }
.section-sub { color: var(--text-muted); font-size: .88rem; margin: 0 0 18px 0; }

.q-columns { display: flex; gap: 16px; flex-wrap: wrap; }
.q-col { flex: 1 1 260px; display: flex; flex-direction: column; gap: 10px; }
.q-col h4 { margin: 0 0 4px 0; font-size: .82rem; letter-spacing: .5px; text-transform: uppercase; color: var(--navy-soft); }
.q-card {
  background: #fff; border: 1px solid var(--border); border-radius: 12px;
  padding: 12px 14px; display: flex; gap: 10px; align-items: flex-start;
  font-size: .88rem; line-height: 1.45; box-shadow: var(--shadow-sm);
  transition: transform .2s ease, box-shadow .2s ease;
}
.q-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.q-icon { font-size: 1rem; }

@media (prefers-reduced-motion: reduce) {
  * { animation-duration: .001ms !important; transition-duration: .001ms !important; }
  .reveal { opacity: 1 !important; transform: none !important; }
}
"""
