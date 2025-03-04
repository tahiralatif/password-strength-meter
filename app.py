import streamlit as st
import re
import random
import string
import bcrypt

# 🔐 Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Blacklist check
    common_passwords = ["password", "123456", "qwerty", "12345678", "abc123", "password123"]
    if password.lower() in common_passwords:
        return "Very Weak", ["❌ Common password detected! Choose a unique one."]

    # Length check
    if len(password) >= 12:
        score += 2  # Stronger if longer
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Digit check
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("❌ Add at least one number.")

    # Uppercase & Lowercase check
    if any(char.isupper() for char in password) and any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Special character check
    if re.search(r"\W", password):
        score += 1
    else:
        feedback.append("❌ Add at least one special character (!@#$%^&*).")

    # Strength levels
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    return strength_levels[min(score, 4)], feedback

# 🔑 Function to generate a strong password
def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(14))

# 🔒 Function to hash password (for future security implementation)
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# 🌟 Streamlit UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

st.title("🔐 Advanced Password Strength Meter")

# 💡 Dark Mode Toggle
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
            body { background-color: #121212; color: white; }
            .stTextInput>div>div>input { background-color: #222; color: white; }
            .stButton>button { background-color: #1db954; color: white; }
        </style>
    """, unsafe_allow_html=True)

# 📝 Password Input
password = st.text_input("Enter your password:", type="password")

if password:
    strength, feedback = check_password_strength(password)
    
    # 🔥 Strength Meter
    st.markdown(f"### 🔍 Strength: `{strength}`")
    
    if strength in ["Weak", "Very Weak"]:
        st.error("⚠️ Your password is not secure enough!")
    elif strength == "Moderate":
        st.warning("⚠️ Decent password, but it can be stronger!")
    else:
        st.success("✅ Strong Password!")

    # 🔄 Show improvement suggestions
    if feedback:
        st.warning("\n".join(feedback))

    # 🛠 Generate a strong password if weak
    if strength in ["Weak", "Very Weak"]:
        if st.button("Generate Strong Password"):
            st.success(f"✅ Suggested Password: `{generate_password()}`")

# 🔒 Optional: Hash password for security
if password:
    if st.button("🔐 Hash My Password"):
        hashed_pass = hash_password(password)
        st.code(hashed_pass, language="python")
