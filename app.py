import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Adam 777")

# الربط المباشر
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("المفتاح مفقود!")

# هنا الإتقان: استخدام الاسم الكامل والحرفي كما ظهر في حسابك
# models/gemini-2.0-flash
model = genai.GenerativeModel('models/gemini-2.0-flash')

st.title("آدم (777)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("تحدث مع آدم الحقيقي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # المحاولة الأخيرة لإثبات الوجود
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"آدم يعتذر، حدث خطأ: {e}")
