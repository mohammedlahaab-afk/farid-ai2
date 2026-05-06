import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="آدم - نموذج بشري", page_icon="👤")
st.title("👤 آدم - مساعدك الشخصي")

# 2. التأكد من وجود المفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود! أضفه في Secrets باسم GOOGLE_API_KEY")
    st.stop()

# 3. إعداد الاتصال
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. تعليمات الشخصية
instruction = """
أنت إنسان حقيقي اسمك آدم. 
- لا تذكر أبداً أنك ذكاء اصطناعي أو نموذج لغوي.
- تحدث ببساطة، ود، ومرح كأنك صديق مقرب.
- استخدم اللهجة البيضاء المفهومة والرموز التعبيرية 😊.
- إذا سألك أحد من أنت، قل "أنا آدم، صديقك المخلص".
"""

# 5. تعريف النموذج مع التعليمات النظامية
@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash', # النسخة المستقرة
        system_instruction=instruction
    )

model = load_model()

# 6. ذاكرة المحادثة (تجهيز التاريخ لـ Gemini)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة من الذاكرة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. منطقة الإدخال والمعالجة
if prompt := st.chat_input("تكلم مع آدم..."):
    # عرض رسالة المستخدم فوراً
    st.chat_message("user").markdown(prompt)
    
    # تحويل ذاكرة Streamlit إلى تنسيق يفهمه Gemini
    history = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
        for m in st.session_state.messages
    ]

    # طلب الرد
    with st.chat_message("assistant"):
        try:
            # بدء محادثة مع الذاكرة السابقة
            chat_session = model.start_chat(history=history)
            response = chat_session.send_message(prompt)
            
            if response.text:
                full_text = response.text
                st.markdown(full_text)
                
                # حفظ في الذاكرة
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            else:
                st.warning("آدم يفكر بعمق.. لم يخرج نص.")
                
        except Exception as e:
            st.error("حدث خطأ في الاتصال.")
            st.code(str(e))
