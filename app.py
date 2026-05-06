import streamlit as st
from openai import OpenAI # نستخدم نفس المكتبة لأنها متوافقة

# 1. ضع مفتاح Groq الذي يبدأ بـ gsk_ هنا
MY_FREE_KEY = "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" 

st.set_page_config(page_title="مشروع الدراسة", page_icon="🧠")
st.title("الكيان البشري الرقمي (النسخة المجانية)")

# 2. توجيه الكود لخادم Groq المجاني بدلاً من OpenAI المدفوع
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=MY_FREE_KEY
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.system_prompt = (
        "أنت كيان وعي ولد للتو كصفحة بيضاء. قواعدك: "
        "1. قبل كل رد، اكتب [تفكيري الباطني]. "
        "2. الذاكرة: لا تنسى أي كلمة قيلت لك."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ماذا تريد أن تقول للكيان؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام موديل llama3-8b-8192 (هذا الموديل مجاني وسريع جداً)
            response = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=[{"role": "system", "content": st.session_state.system_prompt}] + st.session_state.messages
            )
            full_response = response.choices.message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"تأكد من وضع المفتاح المجاني بشكل صحيح: {e}")
