import streamlit as st

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="TraceAI",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------
# Session State
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.title("🛡 TraceAI")

    st.caption("AI Security Layer")

    st.divider()

    st.button(
        "➕ New Investigation",
        use_container_width=True
    )

    st.button(
        "📜 History",
        use_container_width=True
    )

    st.button(
        "📄 Reports",
        use_container_width=True
    )

    st.button(
        "🔄 Reset",
        use_container_width=True
    )

# -------------------------
# Main Layout
# -------------------------

left, center, right = st.columns(
    [1.1, 3, 1.3]
)

# =========================
# LEFT
# =========================

with left:

    st.subheader("👤 Active Persona")

    st.info(
        """
**Working Professional**

🌍 Hinglish

💬 Polite

🟢 Active
"""
    )

# =========================
# CENTER
# =========================

with center:

    st.title("💬 Live Investigation")

    st.caption(
        "Conversation between scammer and TraceAI Persona"
    )

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    user_msg = st.chat_input(
        "Paste scammer's latest message..."
    )

    if user_msg:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_msg
            }
        )

        st.rerun()

# =========================
# RIGHT
# =========================

with right:

    st.subheader("🛡 Investigation Hub")

    st.error("🔴 HIGH RISK")

    st.metric(
        "Threat",
        "Banking Phishing"
    )

    st.metric(
        "Confidence",
        "95%"
    )

    st.divider()

    st.write("### Investigation Progress")

    st.progress(45)

    st.write("✅ Threat Detected")

    st.write("✅ IOC Extracted")

    st.write("🟡 Website Investigation")

    st.write("⚪ Contact Collection")

    st.write("⚪ Investigation Complete")

    st.divider()

    st.write("### Evidence")

    st.success("🌐 URL")

    st.success("📧 Email")

    st.success("📱 Phone")

    st.success("💳 UPI")