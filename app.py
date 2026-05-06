import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="آدم - نموذج بشري", page_icon="👤")
st.title("👤 آدم - مساعدك الشخصي")

# 2. التأكد من وجود المفتاح في الخزانة
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود! اذهب إلى Settings ثم Secrets وأضف GOOGLE_API_KEY")
    st.stop()

# 3. إعداد الاتصال بجوجل
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. تعليمات الشخصية (التي تجعل آدم يبدو بشرياً)
instruction = """
أنت إنسان حقيقي اسمك آدم. 
- لا تذكر أنك ذكاء اصطناعي.
- تحدث ببساطة وود ومرح.
- استخدم اللهجة العربية المفهومة والرموز التعبيرية 😊.
"""

# 5. تعريف النموذج (التعديل الأهم لحل خطأ 404)
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        system_instruction=instruction
    )
except Exception as e:
    st.error(f"فشل في إعداد الموديل: {e}")

# 6. ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. منطقة إدخال المستخدم
if prompt := st.chat_input("تكلم مع آدم..."):
    # إضافة رسالة المستخدم للذاكرة والعرض
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # طلب الرد من آدم
    with st.chat_message("assistant"):
        try:
            # توليد الرد
            response = model.generate_content(prompt)
            
            if response.text:
                full_text = response.text
                st.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            else:
                st.warning("لم يتم توليد نص، قد تكون هناك قيود على المحتوى.")
                
        except Exception as e:
            # في حال استمر الخطأ سيظهر هنا بوضوح
            st.error("حدث خطأ تقني، تأكد من أنك استخدمت مفتاحاً جديداً من Google AI Studio.")
            st.code(str(e))
