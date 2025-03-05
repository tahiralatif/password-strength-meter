import streamlit as st
import re
import random
import string

# 🔐 Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Blacklist check
    common_passwords = ["password", "123456", "qwerty", "12345678", "abc123", "password123"]
    if password.lower() in common_passwords:
        return 0, "Very Weak", ["❌ Common password detected! Choose a unique one."]

    # Length check
    if len(password) >= 12:
        score += 2  
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
    strength_levels = ["Very Weak", "Weak", "Moderate", "Good", "Strong", "Very Strong"]
    return min(score, 5), strength_levels[min(score, 5)], feedback

# 🔑 Function to generate a strong password
def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(14))

# 🌟 Streamlit UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="wide")

st.title("🔐 Advanced Password Strength Meter")

# 🎨 Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=100)
st.sidebar.title("🔹 Quick Actions")
st.sidebar.write("Use the tools below to strengthen your password!")

if st.sidebar.button("🔄 Generate Random Password"):
    st.sidebar.success(f"✅ Suggested: `{generate_password()}`")

st.sidebar.markdown("---")
st.sidebar.title("🔹 Password Tips")
st.sidebar.info("✔ Use at least 12 characters\n✔ Include numbers & special symbols\n✔ Avoid common words")

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ by **Tahira Rajput**")

# 📝 Password Input
password = st.text_input("Enter your password:", type="password")

if password:
    score, strength, feedback = check_password_strength(password)
    
    # 🔥 Strength Meter
    st.markdown(f"### 🔍 Strength: `{strength}`")

    # ✅ Progress bar fix
    st.progress(min(score / 5, 1.0))  

    if strength in ["Weak", "Very Weak"]:
        st.error("⚠️ Your password is not secure enough!")
    elif strength == "Moderate":
        st.warning("⚠️ Decent password, but it can be stronger!")
    elif strength == "Good":
        st.info("👍 Your password is good, but still can be improved!")
    else:
        st.success("✅ Strong Password!")

    # 🔄 Show improvement suggestions
    if feedback:
        st.warning("\n".join(feedback))

    # 🛠 Generate a strong password if weak
    if strength in ["Weak", "Very Weak"]:
        # heading
        st.subheader("���️ Generate a stronger password!")
        if st.button("Generate Strong Password"):
            st.success(f"✅ Suggested Password: `{generate_password()}`")
