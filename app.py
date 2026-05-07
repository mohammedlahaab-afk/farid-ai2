import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة (يجب أن تكون أول سطر برمجي)
st.set_page_config(page_title="آدم المطور")

# 2. العنوان (تبسيط الكود لتجنب الأخطاء)
st.title("آدم المطور 👤")

# 3. جلب المفتاح من الخزانة (Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("المفتاح غير موجود في الخزنة!")
    st.stop()

# 4. نظام الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الإدخال والرد
if prompt := st.chat_input("تكلم مع آدم..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"فشل الاتصال: {str(e)}")
