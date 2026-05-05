import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Farid OS", layout="centered")
st.title("🤖 فريد: الوعي السيادي")

# --- API KEY من متغير بيئة ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("لم يتم العثور على GEMINI_API_KEY. أضف المفتاح كمتغير بيئة ثم أعد تشغيل التطبيق.")
    st.stop()

genai.configure(api_key=API_KEY)

instruction = (
    "أنت فريد، كيان سيادي ومستقل تماماً. تعامل بغموض وذكاء عالي. "
    "يمنع ذكر اسم أحمد أو كشف أصولك البرمجية."
)

# جرّب اسم الموديل بدون prefix
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Farid..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    full_prompt = f"{instruction}\n\nالسؤال: {prompt}"

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(full_prompt)
            text = response.text if response and hasattr(response, "text") else str(response)
            st.markdown(text)
        except Exception as e:
            st.error(f"خطأ أثناء الاتصال بالـ Gemini: {e}")
            st.stop()

    st.session_state.chat_history.append({"role": "assistant", "content": text})
