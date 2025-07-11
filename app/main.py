import streamlit as st
import sqlite3, os, sys
from passlib.hash import bcrypt
from PIL import Image
from datetime import date, datetime
import json

# ✅ Fix the import path to access model and utils folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Now you can import your own modules
from model.predict import predict_image
from utils.pdf_report import generate_pdf


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load model metadata
with open("model_metadata.json", "r") as f:
    meta = json.load(f)

DB = os.path.join("app", "users.db")
LOG_DB = os.path.join("app", "user_logs.db")
os.makedirs("app", exist_ok=True)

#–– Helpers ––#
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT, email TEXT, password TEXT
    )""")
    conn.commit()
    conn.close()

def init_logs_db():
    conn = sqlite3.connect(LOG_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        username TEXT,
        image_name TEXT,
        label TEXT,
        confidence REAL,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

# Call it during startup
init_db()
init_logs_db()


def register(username, name, email, pwd):
    h = bcrypt.using(rounds=12).hash(pwd)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, name, email, h))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate(username, pwd):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, password FROM users WHERE username=?", (username,))
    r = c.fetchone()
    conn.close()
    if not r:
        return False, None
    name, hash_pw = r
    if bcrypt.verify(pwd, hash_pw):
        return True, name
    return False, None

#–– UI ––#
st.set_page_config(page_title="MelanoAI", layout="centered")
st.title("🔐 MelanoAI — Login / Register")

# Sidebar Model Info
st.sidebar.markdown("#### 🔢 Model Info")
st.sidebar.markdown(f"**Name:** {meta['model_name']}")
st.sidebar.markdown(f"**Version:** `{meta['version']}`")
st.sidebar.markdown(f"**Trained on:** `{meta['trained_on']}`")

mode = st.sidebar.selectbox("Mode", ["Login", "Register"])

if mode == "Register":
    st.subheader("Create a new account")
    u = st.text_input("Username")
    n = st.text_input("Full Name")
    e = st.text_input("Email")
    p = st.text_input("Password", type="password")
    if st.button("Register"):
        if not u or not p:
            st.error("Username & password required")
        elif register(u, n, e, p):
            st.success("✅ Registered! Switch to Login.")
        else:
            st.error("⚠️ Username already taken.")
else:
    st.subheader("Login to your account")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        ok, name = authenticate(u, p)
        if not ok:
            st.error("❌ Invalid credentials")
        else:
            st.session_state.user = u
            st.session_state.name = name

#–– After Login ––#
if st.session_state.get("user"):
    st.success(f"Welcome back, {st.session_state.name}!")
    st.header("🖼️ Upload an image for diagnosis")
    img_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    if img_file:
        img = Image.open(img_file).convert("RGB")
        tmp = os.path.join("data", "tmp.jpg")
        os.makedirs("data", exist_ok=True)
        img.save(tmp)
        st.image(img, width=300)

        label, conf, _ = predict_image(tmp)

        st.markdown(f"### 🧬 Prediction: **{label.upper()}**")
        st.markdown(f"**Confidence:** `{conf:.2%}`")

        # Log the prediction
        conn = sqlite3.connect(LOG_DB)
        c = conn.cursor()
        c.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)",
                  (st.session_state.user, img_file.name, label, conf, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

        # PDF Report
        pdf_path = generate_pdf(label, conf, tmp, meta)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Diagnosis Report",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )

    # Show past logs
    st.markdown("---")
    st.markdown("## 📊 Your Prediction History")
    conn = sqlite3.connect(LOG_DB)
    c = conn.cursor()
    c.execute("SELECT image_name, label, confidence, timestamp FROM logs WHERE username=? ORDER BY timestamp DESC", (st.session_state.user,))
    rows = c.fetchall()
    conn.close()

    if rows:
        st.table([{"Image": r[0], "Label": r[1], "Confidence": f"{r[2]*100:.2f}%", "Time": r[3]} for r in rows])
    else:
        st.info("No predictions yet.")
