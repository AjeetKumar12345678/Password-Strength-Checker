 
import streamlit as st
import re
import math
import string
import hashlib

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="SecureCheck | ISS Project",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# PROFESSIONAL CYBERSECURITY UI
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at top left, #102b43 0%, transparent 45%),
        radial-gradient(ellipse at bottom right, #132b2d 0%, transparent 40%),
        #080d18;
    color: #edf3ff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 35px 15px 25px 15px;
}

.logo {
    display: inline-block;
    padding: 10px 18px;
    border: 1px solid #24425d;
    border-radius: 50px;
    background: rgba(23, 48, 72, 0.55);
    color: #55d6be;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero h1 {
    color: #f3f7ff;
    font-size: clamp(34px, 5vw, 52px);
    font-weight: 800;
    letter-spacing: -2px;
    margin: 22px 0 10px 0;
}

.hero h1 span {
    color: #55d6be;
}

.hero p {
    color: #94a6bf;
    font-size: 15px;
    line-height: 1.8;
}

.panel {
    background: rgba(16, 25, 42, 0.92);
    border: 1px solid #26364e;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
}

.panel-title {
    font-size: 18px;
    font-weight: 700;
    color: #f3f7ff;
    margin-bottom: 7px;
}

.panel-subtitle {
    font-size: 13px;
    color: #94a6bf;
    margin-bottom: 20px;
}

.result-card {
    background: linear-gradient(
        145deg,
        rgba(24, 43, 65, 0.98),
        rgba(13, 24, 40, 0.98)
    );
    border: 1px solid #2b4661;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
}

.result-label {
    color: #9aacc5;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.result-status {
    font-size: 32px;
    font-weight: 800;
    margin: 10px 0;
}

.result-description {
    color: #a5b5cb;
    font-size: 13px;
    line-height: 1.7;
}

.metric-card {
    background: rgba(19, 31, 49, 0.92);
    border: 1px solid #283a53;
    border-radius: 14px;
    padding: 18px 12px;
    text-align: center;
    min-height: 105px;
}

.metric-number {
    color: #55d6be;
    font-size: 25px;
    font-weight: 800;
}

.metric-label {
    color: #91a3bb;
    font-size: 12px;
    margin-top: 6px;
}

.check-row {
    background: rgba(24, 38, 57, 0.65);
    border: 1px solid #263950;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 9px 0;
    font-size: 13px;
}

.tip {
    background: rgba(85, 214, 190, 0.07);
    border-left: 3px solid #55d6be;
    padding: 13px 15px;
    border-radius: 5px;
    margin: 10px 0;
    color: #c1d2e5;
    font-size: 13px;
    line-height: 1.7;
}

.footer {
    text-align: center;
    padding: 25px 10px;
    color: #71839d;
    font-size: 12px;
    border-top: 1px solid #1d2a3d;
    margin-top: 35px;
}

div[data-testid="stTextInput"] input {
    background: #0b1423 !important;
    color: #f2f6ff !important;
    border: 1px solid #334760 !important;
    border-radius: 10px !important;
    min-height: 48px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #55d6be !important;
    box-shadow: 0 0 0 1px #55d6be !important;
}

.stButton > button {
    border-radius: 10px;
    min-height: 43px;
    font-weight: 600;
}

.stProgress > div > div > div > div {
    background-color: #55d6be;
}

section[data-testid="stSidebar"] {
    background: #0d1625;
}

#MainMenu, footer {
    visibility: hidden;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .panel {
        padding: 17px;
    }

    .hero h1 {
        letter-spacing: -1px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================
# PASSWORD ANALYSIS ENGINE
# =========================
def analyze_password(password):
    if not password:
        return {
            "score": 0,
            "strength": "Not Tested",
            "color": "#94a6bf",
            "checks": [],
            "tips": ["Enter a password to begin the security assessment."],
            "entropy": 0,
            "length": 0
        }

    length = len(password)

    checks = [
        ("At least 12 characters", length >= 12),
        ("Uppercase letter (A–Z)", bool(re.search(r"[A-Z]", password))),
        ("Lowercase letter (a–z)", bool(re.search(r"[a-z]", password))),
        ("Number (0–9)", bool(re.search(r"[0-9]", password))),
        (
            "Special character",
            any(c in string.punctuation for c in password)
        ),
        ("At least 16 characters", length >= 16)
    ]

    score = 0

    # Length contributes more than simply adding character types.
    if length >= 8:
        score += 1
    if length >= 12:
        score += 2
    if length >= 16:
        score += 2
    if length >= 20:
        score += 1

    # Character diversity.
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    # Penalize common or predictable patterns.
    lower = password.lower()

    common_passwords = {
        "password", "password123", "admin", "admin123",
        "123456", "12345678", "qwerty", "qwerty123",
        "letmein", "iloveyou", "welcome", "abc123"
    }

    if lower in common_passwords:
        score = 0

    predictable_patterns = [
        r"(.)\1{3,}",                 # Four or more repeated characters
        r"1234|2345|3456|4567|5678|6789",
        r"abcd|bcde|cdef|qwerty"
    ]

    if any(re.search(pattern, lower) for pattern in predictable_patterns):
        score = max(0, score - 2)

    # This is an educational heuristic, not a formal security audit.
    if lower in common_passwords or length < 8 or score <= 3:
        strength = "Weak"
        color = "#ff6b78"
    elif length >= 16 and score >= 9:
        strength = "Very Strong"
        color = "#55d6be"
    elif length >= 12 and score >= 7:
        strength = "Strong"
        color = "#65d98a"
    else:
        strength = "Medium"
        color = "#ffbd59"

    # Rough entropy estimate based on character pool.
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    if any(not c.isalnum() and c not in string.punctuation for c in password):
        pool += 20

    entropy = round(length * math.log2(pool), 1) if pool > 0 else 0

    tips = []

    if length < 12:
        tips.append("Use a longer password. Aim for at least 12–16 characters.")
    if length < 16:
        tips.append("Consider using a longer, unique passphrase.")
    if not re.search(r"[a-z]", password):
        tips.append("Include lowercase letters if they fit your password strategy.")
    if not re.search(r"[A-Z]", password):
        tips.append("Consider adding uppercase letters.")
    if not re.search(r"[0-9]", password):
        tips.append("Consider including numbers.")
    if not any(c in string.punctuation for c in password):
        tips.append("Consider including special characters.")
    if lower in common_passwords:
        tips.append("This is a commonly used password. Replace it with a unique one.")
    if any(re.search(pattern, lower) for pattern in predictable_patterns):
        tips.append("Avoid repeated characters and predictable sequences.")

    if not tips:
        tips.append(
            "Good structure. Make sure this password is unique and not reused "
            "on other websites."
        )

    return {
        "score": min(score, 10),
        "strength": strength,
        "color": color,
        "checks": checks,
        "tips": tips,
        "entropy": entropy,
        "length": length
    }


# =========================
# HEADER
# =========================
st.markdown("""
<div class="hero">
    <div class="logo">INFORMATION SECURITY SYSTEMS • ISS</div>
    <h1>Secure<span>Check</span></h1>
    <p>
        Password Strength Analyzer<br>
        Evaluate password characteristics and learn how to improve your security.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# MAIN LAYOUT
# =========================
left, right = st.columns([1.08, 0.92], gap="large")

with left:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">🔐 Password Analyzer</div>
        <div class="panel-subtitle">
            Enter a password to evaluate its characteristics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input(
        "Enter your password",
        type="password",
        placeholder="Type a test password...",
        help="For safety, use a sample password rather than your real account password."
    )

    show_password = st.checkbox("Show password")

    if show_password and password:
        st.code(password, language=None)

    result = analyze_password(password)

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Password Strength</div>
            <div class="result-status" style="color:{result['color']}">
                {result['strength']}
            </div>
            <div class="result-description">
                {"Assessment based on length, character variety and predictable patterns."
                if password else
                "Your assessment will appear here when you enter a password."}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("**Strength Indicator**")

    st.progress(
        result["score"] / 10,
        text=f"{result['score']}/10 heuristic score"
    )

    st.caption(
        "This score is an educational estimate, not a guarantee against attacks."
    )

    st.markdown("""
    <div class="panel-title" style="margin-top:25px;">
        Password Requirements
    </div>
    """, unsafe_allow_html=True)

    if password:
        for label, passed in result["checks"]:
            icon = "✓" if passed else "○"
            color = "#65d98a" if passed else "#94a6bf"

            st.markdown(
                f"""
                <div class="check-row">
                    <span style="color:{color};font-weight:800;">{icon}</span>
                    &nbsp; {label}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("Enter a password to evaluate the requirements.")


with right:
    st.markdown("""
    <div class="panel-title">Security Overview</div>
    <div class="panel-subtitle">
        A quick summary of the password you entered.
    </div>
    """, unsafe_allow_html=True)

    metric1, metric2 = st.columns(2)

    with metric1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">{result['length']}</div>
                <div class="metric-label">Characters</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with metric2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">{len([x for x in result['checks'] if x[1]])}/6</div>
                <div class="metric-label">Requirements Met</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">💡 Security Recommendations</div>
        <div class="panel-subtitle">
            Practical steps to improve password security.
        </div>
    </div>
    """, unsafe_allow_html=True)

    for tip in result["tips"]:
        st.markdown(
            f'<div class="tip">↗ &nbsp; {tip}</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("What makes a password secure?"):
        st.markdown("""
        - **Length:** Prefer long passwords or passphrases.
        - **Uniqueness:** Use a different password for every account.
        - **Unpredictability:** Avoid names, birthdays and common patterns.
        - **Password manager:** Generate and store unique passwords securely.
        - **Multi-factor authentication:** Enable MFA wherever possible.
        """)

    with st.expander("About this ISS project"):
        st.markdown("""
        **Project:** Password Strength Checker

        **Domain:** Information Security Systems

        **Language:** Python

        **Framework:** Streamlit

        **Purpose:** Demonstrate password-strength assessment and
        secure password practices.

        **Privacy:** Password analysis runs in this application.
        This code does not intentionally save passwords to a database
        or send them to an external password-checking service.
        """)


# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    SECURECHECK · ISS MINI PROJECT<br><br>
    Educational cybersecurity tool · Use sample passwords for testing<br>
    Password strength estimates cannot guarantee security.
</div>
""", unsafe_allow_html=True)

