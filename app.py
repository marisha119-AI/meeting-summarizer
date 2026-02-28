import streamlit as st
from openai import OpenAI
import os
import pandas as pd
import re
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# ── SECURE API KEY HANDLER ────────────────────────────────
def get_api_key():
    # First try Streamlit Secrets (for cloud)
    try:
        key = st.secrets["OPENROUTER_API_KEY"]
        if key:
            return key
    except:
        pass
    # Then try .env file (for local)
    try:
        key = os.getenv("OPENROUTER_API_KEY", "")
        if key:
            return key
    except:
        pass
    return None

api_key = get_api_key()

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Executive Meeting Intelligence",
    page_icon="🎯",
    layout="wide"
)

# ── Block app if key not found ────────────────────────────
if not api_key:
    st.markdown("""
    <div style="background:#1e2130; padding:40px; border-radius:15px; text-align:center;">
        <h2 style="color:#ff4444;">⚠️ Configuration Required</h2>
        <p style="color:#aaa;">Please contact the app administrator.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .executive-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d47a1 100%);
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
    }
    .executive-header h1 {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    .executive-header p {
        color: #90caf9;
        margin: 8px 0 0 0;
        font-size: 1rem;
    }
    div[data-testid="metric-container"] {
        background: #1e2130;
        border: 1px solid #2d3561;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div class="executive-header">
    <h1>🎯 Executive Meeting Intelligence</h1>
    <p>Transform meeting transcripts into high-signal executive insights</p>
    <p style="color:#64b5f6; font-size:0.85rem; margin-top:8px;">
        Built by Marisha Dwivedi | AI Engineer Portfolio
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar - NO API KEY SHOWN ANYWHERE ──────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    model_choice = st.selectbox(
    "AI Model (All Free ✅)",
    [
        "z-ai/glm-4.5-air:free",
        "openrouter/auto",
        "deepseek/deepseek-r1:free",
        "deepseek/deepseek-chat-v3-0324:free",
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ]
)
    st.info("💡 Switch model if you get a 429 error!")

    st.markdown("---")
    st.markdown("### 📌 What This Produces")
    st.markdown("""
    - 📊 Executive Overview
    - 📝 30-Second TL;DR Summary
    - ✅ Sortable Action Item Table
    - 🎯 Key Decisions Made
    - ⏱️ Strategic Next Steps
    - ⚠️ Risks & Blockers
    - 📥 Download Report
    """)

    st.markdown("---")
    st.markdown("### 👩‍💻 About")
    st.markdown("""
    Built by **Marisha Dwivedi**
    
    AI Engineer | Prompt Engineering
    
    🔗 [GitHub](https://github.com/marisha119-AI)
    """)

# ── Sample Transcript ─────────────────────────────────────
sample_transcript = """
Meeting: Q3 Product Planning
Date: Monday 10 AM
Attendees: Sarah (PM), John (Dev Lead), Lisa (Designer), Mike (Marketing)

Sarah: Okay let's get started. We need to finalize the Q3 roadmap today.
John: The backend for the new dashboard is 80% done. Ready to test by next Friday.
Lisa: I finished the mockups for the mobile app. I'll send them to John by tomorrow.
Sarah: Great. Mike, what's the status on the marketing campaign?
Mike: We're behind schedule. Need the final product screenshots first. Can Lisa send those by Wednesday?
Lisa: Yes I can do Wednesday for the screenshots.
Sarah: John, can you make sure the demo environment is ready by Thursday?
John: Thursday works. I'll also need someone to review the API documentation. Can Sarah do that by Friday?
Sarah: I'll review the API docs by Friday. We've decided to push the mobile app launch to August 15th.
Mike: That works for marketing.
Sarah: Let's meet again next Monday at 10 AM. Any blockers?
John: No blockers from dev side.
Lisa: No blockers.
Mike: Just need those screenshots by Wednesday.
Sarah: Alright, we're done. Thanks everyone.
"""

# ── Main Input ────────────────────────────────────────────
col_input1, col_input2 = st.columns([2, 1])

with col_input1:
    st.subheader("📋 Meeting Transcript")
    transcript_input = st.text_area(
        "Paste transcript here",
        value=sample_transcript,
        height=280,
        label_visibility="collapsed"
    )

with col_input2:
    st.subheader("⚙️ Meeting Details")
    meeting_name = st.text_input("Meeting Name", value="Q3 Product Planning")
    your_name    = st.text_input("Your Name", value="Sarah")
    meeting_date = st.text_input("Meeting Date", value="Monday 10 AM")
    st.markdown("---")
    st.markdown("**💡 Tips:**")
    st.markdown("• Paste any meeting transcript")
    st.markdown("• Your tasks will be highlighted")
    st.markdown("• Download full report after")

# ── Analyze Button ────────────────────────────────────────
st.markdown("")
analyze_btn = st.button(
    "🚀 Generate Executive Intelligence Report",
    type="primary",
    use_container_width=True
)

if analyze_btn:

    if not transcript_input.strip():
        st.warning("⚠️ Please paste a meeting transcript!")
        st.stop()

    # API key is hidden - comes from secrets or .env only!
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    system_prompt = """
# ROLE
You are the Principal Strategy Analyst. Transform meeting transcripts
into high-signal executive intelligence.

# OUTPUT FORMAT (MANDATORY - follow exactly)
MEETING_OBJECTIVE: (One sentence summary)
SENTIMENT: (Productive / Neutral / Tense / Unresolved)
CONFIDENCE: (0-100)

TLDR_1: (Key insight 1)
TLDR_2: (Key insight 2)
TLDR_3: (Key insight 3)

ACTION_ITEM_START
Task: (description) | Owner: (name) | Deadline: (date or TBD) | Priority: (High/Medium/Low)
Task: (description) | Owner: (name) | Deadline: (date or TBD) | Priority: (High/Medium/Low)
ACTION_ITEM_END

DECISION_1: (Decision name): (Explanation)
DECISION_2: (Decision name): (Explanation)
DECISION_3: (Decision name): (Explanation)

NEXT_MEETING: (Proposed date and agenda)
RISKS: (Risks or blockers. If none write: No blockers identified)

# RULES
- NO conversational filler
- TBD if deadline unknown
- Professional corporate English
- Active verbs only
"""

    user_prompt = f"""
Meeting Name: {meeting_name}
Meeting Date: {meeting_date}
Highlight tasks for: {your_name}

Transcript:
---
{transcript_input}
---
"""

    with st.spinner("🤖 Generating Executive Intelligence Report..."):
        try:
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=1500,
                timeout=60
            )

            result = response.choices[0].message.content.strip()

            # ── Parse Results ──────────────────────────────
            def extract(label, text):
                match = re.search(rf"{label}:\s*(.+)", text)
                return match.group(1).strip() if match else "TBD"

            meeting_obj  = extract("MEETING_OBJECTIVE", result)
            sentiment    = extract("SENTIMENT", result)
            confidence   = extract("CONFIDENCE", result)
            tldr1        = extract("TLDR_1", result)
            tldr2        = extract("TLDR_2", result)
            tldr3        = extract("TLDR_3", result)
            next_meeting = extract("NEXT_MEETING", result)
            risks        = extract("RISKS", result)

            decisions = []
            for i in range(1, 6):
                d = extract(f"DECISION_{i}", result)
                if d != "TBD":
                    decisions.append(d)

            action_items = []
            in_actions = False
            for line in result.split('\n'):
                if "ACTION_ITEM_START" in line:
                    in_actions = True
                    continue
                if "ACTION_ITEM_END" in line:
                    in_actions = False
                    continue
                if in_actions and "Task:" in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        action_items.append({
                            "Task":     parts[0].replace("Task:", "").strip(),
                            "Owner":    parts[1].replace("Owner:", "").strip(),
                            "Deadline": parts[2].replace("Deadline:", "").strip(),
                            "Priority": parts[3].replace("Priority:", "").strip()
                        })

            # ── Display Results ────────────────────────────
            st.markdown("---")
            st.markdown(f"## 📊 Executive Report — {meeting_name}")

            sentiment_map = {
                "Productive": "🟢",
                "Neutral":    "🟡",
                "Tense":      "🔴",
                "Unresolved": "🟠"
            }
            s_icon = sentiment_map.get(sentiment, "⚪")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Meeting Sentiment", f"{s_icon} {sentiment}")
            with col2:
                st.metric("Confidence Score",  f"{confidence}%")
            with col3:
                st.metric("Action Items Found", f"📋 {len(action_items)}")

            st.info(f"**🎯 Objective:** {meeting_obj}")

            st.markdown("### 📝 30-Second TL;DR")
            st.markdown(f"• {tldr1}")
            st.markdown(f"• {tldr2}")
            st.markdown(f"• {tldr3}")

            if action_items:
                st.markdown("### ✅ Action Item Tracker")
                df = pd.DataFrame(action_items)

                def highlight_priority(val):
                    colors = {
                        "High":   "background-color:#7f1d1d; color:#fca5a5;",
                        "Medium": "background-color:#78350f; color:#fcd34d;",
                        "Low":    "background-color:#14532d; color:#86efac;"
                    }
                    return colors.get(val, "")

                def highlight_owner(val):
                    if your_name.lower() in val.lower():
                        return "background-color:#1e3a5f; color:#90caf9; font-weight:bold;"
                    return ""

                styled_df = df.style\
                    .applymap(highlight_priority, subset=["Priority"])\
                    .applymap(highlight_owner,    subset=["Owner"])

                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True
                )
                st.caption(f"💡 Blue highlighted rows = {your_name}'s tasks")

            if decisions:
                st.markdown("### 🎯 Key Decisions Made")
                for d in decisions:
                    if d and d != "TBD":
                        st.success(f"✅ {d}")

            col_n, col_r = st.columns(2)
            with col_n:
                st.markdown("### ⏱️ Next Meeting")
                st.info(f"📅 {next_meeting}")
            with col_r:
                st.markdown("### ⚠️ Risks & Blockers")
                if "no blockers" in risks.lower():
                    st.success(f"✅ {risks}")
                else:
                    st.error(f"🚨 {risks}")

            # ── Download Buttons ───────────────────────────
            st.markdown("---")
            action_text    = "\n".join([
                f"• {i['Task']} | {i['Owner']} | {i['Deadline']} | {i['Priority']}"
                for i in action_items
            ]) if action_items else "No action items found"
            decisions_text = "\n".join([
                f"• {d}" for d in decisions
            ]) if decisions else "No decisions recorded"

            full_report = f"""
EXECUTIVE MEETING INTELLIGENCE REPORT
======================================
Meeting   : {meeting_name}
Date      : {meeting_date}
Sentiment : {sentiment}
Confidence: {confidence}%

OBJECTIVE
---------
{meeting_obj}

TL;DR SUMMARY
-------------
- {tldr1}
- {tldr2}
- {tldr3}

ACTION ITEMS
------------
{action_text}

KEY DECISIONS
-------------
{decisions_text}

NEXT MEETING
------------
{next_meeting}

RISKS & BLOCKERS
----------------
{risks}

======================================
Generated by Executive Meeting Intelligence
Built by Marisha Dwivedi | AI Engineer
GitHub: https://github.com/marisha119-AI
"""

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button(
                    "📥 Download Report (.txt)",
                    data=full_report,
                    file_name=f"{meeting_name}_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col_d2:
                if action_items:
                    csv = pd.DataFrame(action_items).to_csv(index=False)
                    st.download_button(
                        "📊 Download Actions (.csv)",
                        data=csv,
                        file_name=f"{meeting_name}_actions.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

            st.success("✅ Executive Intelligence Report Complete!")

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.error("❌ Model busy!")
                st.warning("👉 Switch model in sidebar!")
            elif "401" in error_msg:
                st.error("❌ API Key error - contact admin!")
            elif "404" in error_msg:
                st.error("❌ Model not found!")
                st.warning("👉 Switch to openrouter/auto!")
            else:
                st.error(f"❌ Error: {error_msg}")

# ── Footer ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#666;'>Built by Marisha Dwivedi | AI Engineer Portfolio | Streamlit + OpenRouter</center>",
    unsafe_allow_html=True
)
