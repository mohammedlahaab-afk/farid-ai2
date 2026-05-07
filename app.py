import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="آدم المطور", page_icon="👤")

# تحسين مظهر العنوان
st.markdown("<h1 style='text-align: right;'>آدم المطور 👤</h1>", unsafe_allow_context=True)

# 2. جلب المفتاح من الخزانة (Secrets)
try:
    # تأكد أن الاسم في الخزانة هو GOOGLE_API_KEY
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("خطأ: لم يتم العثور على المفتاح في الخزنة. تأكد من إضافته في إعدادات Streamlit.")
    st.stop()

# 3. دالة المحادثة
def generate_ai_response(prompt):
    try:
        # استخدام الموديل المطلوب
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"عذراً، حدث خطأ أثناء الاتصال بالسيرفر: {str(e)}"

# 4. نظام الذاكرة للمحادثة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة بتنسيق جميل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال (Chat Input)
if prompt := st.chat_input("تكلم مع آدم..."):
    # إضافة رسالة المستخدم للذاكرة وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("آدم يفكر..."):
            full_response = generate_ai_response(prompt)
            st.markdown(full_response)
    
    # إضافة رد المساعد للذاكرة
    st.session_state.messages.append({"role": "assistant", "content": full_response})
