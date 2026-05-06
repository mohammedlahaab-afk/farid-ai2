import streamlit as st
import google.generativeai as genai

# إعداد واجهة التطبيق
st.set_page_config(page_title="آدم")
st.title("👤 آدم - نموذج بشري")

# التحقق من المفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود من الخزانة (Secrets)!")
    st.stop()

# إعداد المكتبة
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# تعليمات آدم
instruction = "أنت إنسان حقيقي اسمك آدم، تحدث بلهجة ودودة وبسيطة."

# محاولة تعريف الموديل
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )
except Exception as e:
    st.error(f"فشل في إعداد الموديل: {e}")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("تكلم مع آدم..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        try:
            # طلب بسيط ومباشر
            response = model.generate_content(prompt)
            
            if response.text:
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("رد جوجل فارغ، ربما هناك قيود على المحتوى.")
                
        except Exception as e:
            # هنا سنعرف السبب الحقيقي
            st.error("تفاصيل الخطأ التقني:")
            st.code(str(e))
