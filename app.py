import streamlit as st
import google.generativeai as genai

# إعداد المفتاح
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# استخدام الموديل الصحيح 1.5 flash
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("آدم المطور 👤")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تكلم مع آدم..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ: {e}")
