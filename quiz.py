import streamlit as st
import random
import requests
import time
from database import register_user, authenticate_user, save_score, get_leaderboard

# ✅ Set Page Configuration
st.set_page_config(page_title="🎯 Advanced Quiz App", layout="centered")

st.title("🎯 Advanced Quiz App")

# ✅ Authentication System
if "user" not in st.session_state:
    st.session_state.user = None

def login():
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    if st.button("🔓 Login"):
        if authenticate_user(username, password):
            st.session_state.user = username
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Incorrect username or password!")

def signup():
    username = st.text_input("👤 Choose a Username")
    password = st.text_input("🔑 Choose a Password", type="password")
    if st.button("🆕 Sign Up"):
        if register_user(username, password):
            st.success("✅ Account created! Please login.")
        else:
            st.error("❌ Username already exists!")

# ✅ Show Authentication Options
if not st.session_state.user:
    auth_choice = st.radio("Select:", ["🔓 Login", "🆕 Sign Up"])
    if auth_choice == "🔓 Login":
        login()
    else:
        signup()
    st.stop()

st.success(f"🎉 Logged in as {st.session_state.user}")

# ✅ Fetch Quiz Questions from API
def fetch_questions():
    url = "https://opentdb.com/api.php?amount=5&type=multiple"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["results"]
        questions = []
        for item in data:
            options = item["incorrect_answers"] + [item["correct_answer"]]
            random.shuffle(options)
            questions.append({
                "question": item["question"],
                "options": options,
                "answer": item["correct_answer"]
            })
        return questions
    return []

# ✅ Initialize Quiz Session
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = fetch_questions()
    random.shuffle(st.session_state.quiz_data)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# ✅ Timer
time_left = 20 - (time.time() - st.session_state.start_time)
if time_left <= 0:
    st.session_state.quiz_complete = True
    st.warning("⏳ Time's up!")

# ✅ Quiz Navigation System
if not st.session_state.quiz_complete:
    question_data = st.session_state.quiz_data[st.session_state.question_index]
    st.subheader(f"🔹 {question_data['question']}")
    
    user_answer = st.radio("📌 Choose an answer:", question_data["options"])
    st.markdown(f"<p style='color:red;'>⏳ Time left: {int(time_left)}s</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.question_index == 0):
            st.session_state.question_index -= 1
            st.session_state.start_time = time.time()
            st.rerun()

    with col2:
        if st.button("✅ Submit Answer"):
            if user_answer == question_data["answer"]:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! The correct answer was **{question_data['answer']}**.")
            
            time.sleep(1)
            if st.session_state.question_index < len(st.session_state.quiz_data) - 1:
                st.session_state.question_index += 1
                st.session_state.start_time = time.time()
            else:
                st.session_state.quiz_complete = True
            st.rerun()

    with col3:
        if st.button("➡️ Next", disabled=st.session_state.question_index == len(st.session_state.quiz_data) - 1):
            st.session_state.question_index += 1
            st.session_state.start_time = time.time()
            st.rerun()

else:
    st.subheader(f"🏆 Quiz Completed! Your Score: {st.session_state.score} / {len(st.session_state.quiz_data)}")
    st.progress(st.session_state.score / len(st.session_state.quiz_data))

    # ✅ Save Score in Database
    if st.button("💾 Save Score"):
        save_score(st.session_state.user, st.session_state.score)
        st.success("✅ Score saved!")

    # ✅ Display Leaderboard
    st.subheader("🏅 Leaderboard")
    leaderboard = get_leaderboard()
    for rank, (username, score) in enumerate(leaderboard, start=1):
        st.write(f"**{rank}. {username}** - {score} points")

    if st.button("🔄 Try Again"):
        st.session_state.score = 0
        st.session_state.question_index = 0
        st.session_state.quiz_complete = False
        st.session_state.quiz_data = fetch_questions()
        st.session_state.start_time = time.time()
        st.rerun()

# ✅ Footer with Icons
st.markdown("""
---
🔹 Developed by **Gini Technology** | 🚀 Follow us on [LinkedIn](www.linkedin.com/in/ch-usman-213807309) 🌎
""", unsafe_allow_html=True)
