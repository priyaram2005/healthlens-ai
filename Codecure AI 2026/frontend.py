import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import fitz

def calculate_health_score(analysis):
    score = 100

    for status in analysis.values():
        if status == "High":
            score -= 20
        elif status == "Low":
            score -= 10

    return max(score, 0)

st.set_page_config(layout="wide")

# -------------------------
# STYLING
# -------------------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #e0f7fa, #fce4ec);
}

/* GLASS CARD */
.glass-card {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);

    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.3);

    padding: 12px;
    text-align: center;
    margin-bottom: 25px;

    box-shadow: 0 8px 25px rgba(0,0,0,0.08);

    transition: all 0.25s ease;
}

/* HOVER EFFECT */
.glass-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}

/* RISK CARD */
.glass-risk {
    background: rgba(255,255,255,0.3);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.4);
    padding: 18px;
    margin-bottom: 25px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* TITLE POLISH */
.title-glow {
    text-align: center;
    font-weight: 800;
    letter-spacing: 0.5px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------
st.markdown("""
<h1 class='title-glow'>
🧠 AI Health Intelligence Dashboard
</h1>
<p style='text-align:center; color:black; margin-top:-10px;'>
Turning Reports into Smart Health Insights 🚀
</p>
""", unsafe_allow_html=True)

# -------------------------
# INPUT
# -------------------------
st.sidebar.header("📄 Input")

option = st.sidebar.radio("Choose Input Type", ["Paste Text", "Upload PDF"])
report_text = ""

if option == "Paste Text":
    report_text = st.sidebar.text_area("Paste your report")

else:
    file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
    if file:
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            report_text += page.get_text()
        st.sidebar.success("✅ PDF processed")

analyze = st.sidebar.button("📈 Analyze")

# -------------------------
# MAIN OUTPUT
# -------------------------
if analyze and report_text:

    with st.spinner("Analyzing..."):
        res = requests.post(
            "http://127.0.0.1:5000/analyze",
            json={"report_text": report_text}
        )
        data = res.json()

    params = data["parameters"]
    analysis = data["analysis"]
    risk = data["risk"]
    recs = data["recommendations"]

    score = calculate_health_score(analysis)

    st.subheader("Health Score")
    st.markdown("""
    <p style="color:#6c63ff; font-weight:500; margin-bottom:5px;">
    🔍 Analyzing your health metrics...
    </p>
    """, unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title = {
            'text': "<span style='color:#333;'>Overall Health Score</span>"
        },
        number={'font': {'color': '#000000'}},
        
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2ecc71" if score > 70 else "#ffb84d" if score > 40 else "#ff4d4d"},
            'steps': [
                {'range': [0, 40], 'color': '#ffe6e6'},
                {'range': [40, 70], 'color': '#fff3e6'},
                {'range': [70, 100], 'color': '#eafaf1'}
            ]
        }
    ))

    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    with st.container():
        st.markdown("""
        <style>
        div[data-testid="stPlotlyChart"] {
            background: rgba(255,255,255);
            # backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 10px;
            border: 1px solid rgba(255,255,255,0.4);
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        </style>
        """, unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # 🚨 RISK CARD
    # -------------------------
    color_map = {
        "Low": "#00c853",
        "Moderate": "#ff9800",
        "High": "#ff1744"
    }

    st.markdown(f"""
    <div class="glass-risk">
        <h3 style="margin:0;">🚨 Risk Level:
            <span style="color:{color_map[risk]};">{risk}</span>
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 🧪 PARAMETERS GRID
    # -------------------------
    st.subheader("🧪 Health Parameters")

    cols = st.columns(len(params))  # auto = 5 cards in 1 row

    for col, (k, v) in zip(cols, params.items()):
        status = analysis.get(k, "Normal")

        if status == "High":
            color = "#ff4d4d"
            emoji = "🔴"
        elif status == "Low":
            color = "#ffb84d"
            emoji = "🟡"
        else:
            color = "#2ecc71"
            emoji = "🟢"

        with col:
            st.markdown(f"""
            <div class="glass-card">
                <p style="margin:0; font-size:15px; font-weight: 500;">{emoji} {k}</p>
                <p style="margin:4px 0; font-size:18px; font-weight:600;">{v}</p>
                <p style="margin:0; color:{color}; font-size:14px; font-weight: 500;">{status}</p>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------
    # 📊 CHART
    # -------------------------
    st.subheader("📊 Visual Analysis")

    df = pd.DataFrame({
        "Parameter": list(params.keys()),
        "Value": list(params.values()),
        "Status": [analysis[k] for k in params.keys()]
    })

    color_map = {
        "High": "#ff4d4d",
        "Low": "#ffb84d",
        "Normal": "#2ecc71"
    }

    fig = px.bar(
        df,
        x="Parameter",
        y="Value",
        color="Status",
        color_discrete_map=color_map,
        text="Value",
        title="Health Parameter Overview"
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=1.5
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        title_font_size=20,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # 🩺 RECOMMENDATIONS
    # -------------------------
    st.subheader("🩺 Smart Recommendations")

    emoji_map = {
        "iron": "🥬",
        "sugar": "🍬",
        "fat": "🍔",
        "sun": "☀️"
    }

    for r in recs:
        emoji = "💡"
        if "iron" in r.lower():
            emoji = "🥬"
        elif "sugar" in r.lower():
            emoji = "🍬"
        elif "fat" in r.lower():
            emoji = "🍔"
        elif "vitamin d" in r.lower():
            emoji = "☀️"

        st.markdown(f"{emoji} {r}")

    st.info("⚠️ AI-generated insights. Consult a doctor.")

elif analyze:
    st.warning("⚠️ Please provide input")