import streamlit as st
from groq import Groq
import json
import re

# Enter your Groq API Key
client=Groq(api_key="YOUR_GROQ_API_KEY")

st.set_page_config(page_title="AI Quiz Generator", page_icon="📝")

st.title("📝 AI Quiz Generator")

topic = st.text_input("Enter Topic")

difficulty = st.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

num_questions = st.slider(
    "Number of Questions",
    5,
    20,
    10
)

if st.button("Generate Quiz"):

    prompt = f"""
Generate {num_questions} multiple choice questions on the topic "{topic}".

Difficulty: {difficulty}

Return ONLY valid JSON.

Format:

[
 {{
   "question":"Question",
   "options":["A","B","C","D"],
   "answer":"Correct Answer"
 }}
]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    # Remove markdown if present
    result = re.sub(r"```json|```", "", result).strip()

    try:
        quiz = json.loads(result)

        score = 0

        st.header("Quiz")

        for i, q in enumerate(quiz):

            st.subheader(f"Q{i+1}. {q['question']}")

            user = st.radio(
                "Choose Answer",
                q["options"],
                key=i
            )

            if user == q["answer"]:
                score += 1

        if st.button("Show Answers"):

            st.success(f"Your Score: {score}/{len(quiz)}")

            st.header("Correct Answers")

            for i, q in enumerate(quiz):
                st.write(f"**Q{i+1}: {q['question']}**")
                st.write("✅", q["answer"])
                st.write("---")

    except:
        st.error("Invalid response from AI.")
        st.write(result)
