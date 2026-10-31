
import streamlit as st
import sqlite3
import hashlib
import secrets
import re
import html
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Nandu Organization | Welcome",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_NAME = "nandu_users.db"

# --------------------------------------------------
# DATABASE FUNCTIONS
# --------------------------------------------------

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                profession TEXT NOT NULL,
                experience TEXT,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                registered_at TEXT NOT NULL
            )
        """)
        conn.commit()

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        600000
    )

    return hashed.hex(), salt

def register_user(name, email, phone, profession,
                  experience, password):

    password_hash, salt = hash_password(password)

    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO users (
                    full_name, email, phone,
                    profession, experience,
                    password_hash, salt, registered_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, email, phone,
                profession, experience,
                password_hash, salt,
                datetime.now().isoformat()
            ))
            conn.commit()

        return True, "Registration successful!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered."

    except sqlite3.Error:
        return False, "Something went wrong. Please try again."


# --------------------------------------------------
# VALIDATION FUNCTIONS
# --------------------------------------------------

def validate_email(email):
    pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
    return re.match(pattern, email) is not None

def validate_phone(phone):
    digits = re.sub(r"\D", "", phone)
    return len(digits) == 10

def validate_password(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
    )


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #080d24 0%,
        #101a3b 55%,
        #17103a 100%
    );
    color: white;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.hero {
    text-align: center;
    padding: 55px 20px 35px;
}

.hero h1 {
    font-size: clamp(36px, 6vw, 65px);
    font-weight: 800;
    background: linear-gradient(
        90deg, #ffffff, #8b9cff, #d9a7ff
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #c4cbe5;
    font-size: 17px;
    line-height: 1.8;
}

.tag {
    display: inline-block;
    background: #25315e;
    color: #a9b8ff;
    padding: 8px 18px;
    border-radius: 30px;
    font-size: 13px;
    margin-bottom: 12px;
}

.section-title {
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    margin: 35px 0 15px;
    color: #ffffff;
}

.glass-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 18px;
    padding: 25px;
    margin: 10px 0;
    min-height: 160px;
}

.glass-card h3 {
    color: #aebcff;
}

.glass-card p {
    color: #d1d7ed;
    font-size: 14px;
    line-height: 1.7;
}

.success-banner {
    text-align: center;
    background: linear-gradient(
        135deg, #163e51, #29205c
    );
    border: 1px solid #687cff;
    border-radius: 22px;
    padding: 35px 20px;
    margin: 25px 0;
}

.success-banner h1 {
    font-size: clamp(28px, 5vw, 46px);
    color: #ffffff;
}

.success-banner p {
    color: #d8e1ff;
}

.footer {
    text-align: center;
    color: #8791b2;
    padding: 35px 10px;
    font-size: 12px;
}

.stButton > button {
    background: linear-gradient(90deg, #6255ee, #a04eff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 600;
    width: 100%;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #8177ff, #bc75ff);
    transform: translateY(-2px);
    color: white;
}

[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #192343;
    color: white;
}

label {
    color: #e2e7ff !important;
}

@media(max-width: 768px) {
    .hero {
        padding: 30px 10px;
    }

    .hero p {
        font-size: 14px;
    }

    .block-container {
        padding: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INITIALIZE
# --------------------------------------------------

initialize_database()

if "registered" not in st.session_state:
    st.session_state.registered = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">

    <div class="tag">
        🚀 THE FUTURE STARTS HERE
    </div>

    <h1>NANDU ORGANIZATION</h1>

    <p>
        Learn. Build. Innovate. Achieve.<br>
        Join our community and unlock opportunities
        to build your future.
    </p>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Why Join Nandu Organization?</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3>💻 Real Projects</h3>
        <p>Work on practical development projects
        and build your technical portfolio.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3>🚀 Skill Development</h3>
        <p>Explore modern technologies, improve
        your skills and learn by doing.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <h3>🌟 New Opportunities</h3>
        <p>Discover learning opportunities and
        take your career to the next level.</p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# REGISTRATION FORM
# --------------------------------------------------

if not st.session_state.registered:

    st.markdown(
        '<div class="section-title">📝 Register With Us</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Create your account and discover what awaits you!"
    )

    with st.form("registration_form"):

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input(
                "Full Name *",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email Address *",
                placeholder="example@gmail.com"
            )

            phone = st.text_input(
                "Mobile Number *",
                placeholder="10-digit mobile number"
            )

        with col2:
            profession = st.selectbox(
                "Current Profession *",
                [
                    "Select your profession",
                    "Software Engineer",
                    "Frontend Developer",
                    "Backend Developer",
                    "DevOps Engineer",
                    "QA Engineer",
                    "Student",
                    "Other"
                ]
            )

            experience = st.selectbox(
                "Experience",
                [
                    "Fresher",
                    "0-1 Years",
                    "1-3 Years",
                    "3-5 Years",
                    "5+ Years"
                ]
            )

            password = st.text_input(
                "Create Password *",
                type="password",
                placeholder="Minimum 8 characters"
            )

        confirm_password = st.text_input(
            "Confirm Password *",
            type="password",
            placeholder="Re-enter your password"
        )

        terms = st.checkbox(
            "I agree to the registration terms and privacy policy."
        )

        submitted = st.form_submit_button(
            "🚀 JOIN NANDU ORGANIZATION"
        )

        if submitted:

            if not all([
                full_name.strip(),
                email.strip(),
                phone.strip(),
                password,
                confirm_password
            ]):
                st.error("Please complete all required fields.")

            elif profession == "Select your profession":
                st.error("Please select your profession.")

            elif not validate_email(email.strip()):
                st.error("Please enter a valid email address.")

            elif not validate_phone(phone):
                st.error("Enter a valid 10-digit mobile number.")

            elif not validate_password(password):
                st.error(
                    "Password must contain 8 characters, "
                    "one uppercase, one lowercase and one number."
                )

            elif password != confirm_password:
                st.error("Passwords do not match.")

            elif not terms:
                st.error("Please accept the registration terms.")

            else:

                success, message = register_user(
                    full_name.strip(),
                    email.strip().lower(),
                    phone.strip(),
                    profession,
                    experience,
                    password
                )

                if success:

                    st.session_state.registered = True
                    st.session_state.user_name = full_name.strip()
                    st.session_state.user_email = email.strip().lower()

                    st.balloons()
                    st.rerun()

                else:
                    st.error(message)


# --------------------------------------------------
# SUCCESS / PROJECT UNLOCK SCREEN
# --------------------------------------------------

else:

    safe_name = html.escape(st.session_state.user_name)

    st.balloons()

    st.markdown(f"""
    <div class="success-banner">

        <h1>🎉 CONGRATULATIONS, {safe_name.upper()}!</h1>

        <h2>YOU HAVE UNLOCKED EXCLUSIVE PROJECTS! 🔓</h2>

        <p>
            Welcome to Nandu Organization.<br>
            Your journey towards innovation starts today.
        </p>

        <h3>🚀 YOUR NEXT CHAPTER STARTS NOW!</h3>

    </div>
    """, unsafe_allow_html=True)

    st.success(
        f"Registration completed successfully! "
        f"Welcome aboard, {safe_name}."
    )

    st.markdown(
        '<div class="section-title">🔓 Your Unlocked Projects</div>',
        unsafe_allow_html=True
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div class="glass-card">
            <h3>💻 Project 01</h3>
            <h4>Python Automation</h4>
            <p>Build practical automation tools
            using Python and real-world workflows.</p>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="glass-card">
            <h3>☁️ Project 02</h3>
            <h4>DevOps Engineering</h4>
            <p>Explore CI/CD pipelines, Docker,
            Kubernetes and cloud deployment.</p>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div class="glass-card">
            <h3>🌐 Project 03</h3>
            <h4>Web Development</h4>
            <p>Create responsive applications
            using modern web technologies.</p>
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------
    # YOUTUBE VIDEOS
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">🎬 Exclusive Videos</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore these videos as part of your welcome experience."
    )

    video1, video2 = st.columns(2)

    with video1:
        st.subheader("🎥 Video 01")
        st.video(
            "https://www.youtube.com/watch?v=hZeuvfYObqo&t=737s"
        )

    with video2:
        st.subheader("🎥 Video 02")
        st.video(
            "https://www.youtube.com/shorts/9I9DNCM88yI"
        )

    st.markdown("---")

    if st.button("Logout / Back to Registration"):
        st.session_state.registered = False
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    <p>© 2026 Nandu Organization. All Rights Reserved.</p>
    <p>Built with ❤️ using Python & Streamlit</p>
</div>
""", unsafe_allow_html=True)
