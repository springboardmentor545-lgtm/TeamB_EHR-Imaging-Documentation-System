import streamlit as st

# -------- Page Config --------
st.set_page_config(page_title="HeartFlow Portal", layout="wide")

# -------- CSS Styling for cards and gradients --------
st.markdown(
    """
    <style>
    .card {
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: scale(1.05);
    }
    .button {
        background-color: #f5576c;
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
    }
    .button:hover {
        background-color: #f093fb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------- Hero Section --------
st.markdown("<h1 style='text-align: center; color: #f5576c;'>❤️ HeartFlow Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size:18px;'>Advanced Cardiac EHR System for Comprehensive Heart Care Management</p>", unsafe_allow_html=True)

st.write("---")

# -------- Role Cards --------
roles = [
    {
        "title": "Administrator",
        "description": "Manage system, users, and view analytics",
        "features": ["User Management", "System Analytics", "Reports Overview"],
        "endpoint": "admin_portal"
    },
    {
        "title": "Doctor",
        "description": "Access patient records and create reports",
        "features": ["Patient Database", "Report Analysis", "Clinical Tools"],
        "endpoint": "doctor_portal"
    },
    {
        "title": "Patient",
        "description": "View your health records and appointments",
        "features": ["Health Dashboard", "Appointments", "Medical Records"],
        "endpoint": "patient_portal"
    },
]

cols = st.columns(len(roles))

for idx, role in enumerate(roles):
    with cols[idx]:
        st.markdown(f"<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{role['title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{role['description']}</p>", unsafe_allow_html=True)
        st.markdown("<ul>", unsafe_allow_html=True)
        for feat in role['features']:
            st.markdown(f"<li>{feat}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
        if st.button(f"Access {role['title']} Portal", key=role['title']):
            # -------- Backend endpoint hook --------
            st.session_state['current_portal'] = role['endpoint']
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# -------- Feature Highlights --------
st.markdown("<h2 style='text-align: center;'>Comprehensive Cardiac Care Platform</h2>", unsafe_allow_html=True)
features = [
    {"title": "Real-time Analysis", "desc": "Instant cardiac data processing and insights"},
    {"title": "Secure Records", "desc": "HIPAA-compliant patient data management"},
    {"title": "Advanced Imaging", "desc": "CT, MRI, and ECG integration"},
    {"title": "Collaborative Care", "desc": "Seamless communication between providers"},
]

cols = st.columns(2)
for idx, feature in enumerate(features):
    with cols[idx % 2]:
        st.markdown(
            f"<div style='padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;'>"
            f"<h4>{feature['title']}</h4>"
            f"<p>{feature['desc']}</p>"
            f"</div>", unsafe_allow_html=True
        )

# -------- Backend Endpoint Simulation --------
if 'current_portal' in st.session_state:
    endpoint = st.session_state['current_portal']
    st.markdown(f"### You clicked into **{endpoint}**! Connect your backend logic here.")
