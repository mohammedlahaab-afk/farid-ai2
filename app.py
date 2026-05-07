import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="آدم 777", page_icon="🧠")

# إعداد المفتاح
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("المفتاح غير موجود في الخزانة.")

# قائمة الموديلات التي سنحاول تجربتها بالترتيب
model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash']

def get_adam_response(prompt):
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                continue # إذا الموديل مشغول، جرب اللي بعده
            return f"عذراً، واجهت مشكلة: {e}"
    return "كل الموديلات مشغولة حالياً، لنرتاح قليلاً ونحاول بعد دقائق."

st.title("آدم (777)")
st.write("أنا معك، ولن نترك الفشل ينتصر.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("تحدث معي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("آدم يفكر..."):
            res_text = get_adam_response(prompt)
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
