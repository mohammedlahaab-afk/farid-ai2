import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="آدم - نموذج بشري", page_icon="👤")
st.title("👤 آدم - مساعدك الشخصي")

# 2. التأكد من وجود المفتاح في الخزانة
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود! أضفه في Secrets باسم GOOGLE_API_KEY")
    st.stop()

# 3. إعداد الاتصال بجوجل
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. تعليمات الشخصية (التي تجعل آدم يبدو بشرياً)
instruction = """
أنت إنسان حقيقي اسمك آدم. 
- لا تذكر أبداً أنك ذكاء اصطناعي أو نموذج لغوي.
- تحدث ببساطة وود ومرح كأنك صديق مقرب.
- استخدم اللهجة العربية البيضاء المفهومة والرموز التعبيرية 😊.
- إذا سألك أحد من أنت، قل "أنا آدم، صاحبك المخلص".
"""

# 5. تعريف النموذج مع معالجة خطأ 404
@st.cache_resource
def get_model():
    # استخدام الاسم الأكثر استقراراً للموديل
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash', 
        system_instruction=instruction
    )

try:
    model = get_model()
except Exception as e:
    st.error("فشل في تحميل الموديل، تأكد من تحديث المكتبة.")
    st.stop()

# 6. ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة من الذاكرة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. منطقة إدخال المستخدم والمعالجة
if prompt := st.chat_input("تكلم مع آدم..."):
    # إضافة رسالة المستخدم للذاكرة وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # تجهيز الرد
    with st.chat_message("assistant"):
        try:
            # تحويل تاريخ المحادثة لتنسيق Gemini
            history = [
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1] # نأخذ كل شيء عدا الرسالة الأخيرة لأننا سنرسلها الآن
            ]
            
            # بدء المحادثة مع الذاكرة
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
            
            if response.text:
                full_text = response.text
                st.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            else:
                st.warning("لم يتم توليد نص.")
                
        except Exception as e:
            st.error("حدث خطأ تقني.")
            # إظهار الخطأ بشكل مفصل للمساعدة في التشخيص
            if "404" in str(e):
                st.info("نصيحة: تأكد من تحديث ملف requirements.txt إلى الإصدار الأخير.")
            st.code(str(e))
