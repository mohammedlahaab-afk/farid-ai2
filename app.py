import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="آدم - النسخة المستقرة", page_icon="👤")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود في Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# تعليمات آدم مدمجة
instruction = "تعليمات: أنت آدم، إنسان ودود ومرح، تحدث بالعربية البسيطة ولا تقل أنك ذكاء اصطناعي."

# محاولة استخدام الموديل المستقر 1.0 Pro
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"خطأ في الموديل: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("تكلم مع آدم..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # دمج التعليمات مع السؤال لضمان الالتزام بالشخصية في موديل 1.0
            full_prompt = f"{instruction}\n\nالمستخدم يقول: {prompt}"
            response = model.generate_content(full_prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("عذراً، آدم واجه مشكلة في الاتصال.")
            st.code(str(e))
