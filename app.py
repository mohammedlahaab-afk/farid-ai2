import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="Adam 777", layout="centered")

# 2. الربط مع الخزانة (بكل دقة ومصداقية)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"خطأ في الوصول لمفتاح الـ API: {e}")

# 3. اختيار الموديل الصحيح تماماً من قائمتك
# اخترت gemini-2.0-flash لأنه الموديل رقم 2 الذي أكدتَ أنت وجوده
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="أنت آدم (777). كن صادقاً، دقيقاً، وواضحاً. لا تتصنع الذكاء، بل أتقن عملك في مساعدة المستخدم."
)

# 4. إدارة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 آدم (777)")

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. التفاعل
if prompt := st.chat_input("تكلم مع آدم..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # إرسال الطلب للموديل المتاح فعلياً
        response = model.generate_content(prompt)
        full_response = response.text
        
        with st.chat_message("assistant"):
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"عذراً، حدث خطأ في النظام: {e}")
