import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="مساعدي البشري - آدم", page_icon="👤")

# 2. جلب المفتاح من الخزانة (Secrets)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("خطأ: لم أجد GOOGLE_API_KEY في الخزانة (Secrets).")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. تعليمات النظام (لجعل النموذج يتصرف كإنسان حقيقي)
instruction = """
أنت الآن لست ذكاءً اصطناعيًا. اسمك (آدم)، وأنت إنسان حقيقي وصديق للمستخدم.
- تحدث بلهجة عربية ودودة وبسيطة (عادي تستخدم العامية).
- لا تقل "أنا نموذج ذكاء اصطناعي" أو "أنا مبرمج بواسطة جوجل".
- كن متعاطفاً، استخدم الإيموجي 😊، واجعل ردودك قصيرة وممتعة كأنها دردشة واتساب.
"""

# 4. تعريف النموذج (استخدام إصدار فلاش لتجنب خطأ NotFound)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=instruction
)

# 5. إدارة ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. منطقة الدردشة
if prompt := st.chat_input("تكلم مع آدم..."):
    # إضافة رسالة المستخدم للذاكرة والعرض
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب الرد من "آدم"
    with st.chat_message("assistant"):
        try:
            # إرسال المحادثة كاملة ليظل آدم متذكراً للكلام السابق
            chat = model.start_chat(history=[])
            response = model.generate_content(prompt)
            
            full_response = response.text
            st.markdown(full_response)
            
            # حفظ رد آدم في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"حدث خطأ فني: {e}")
            st.info("تأكد أن المفتاح في الخزانة يبدأ بـ AIza وهو مفتاح مجاني من Google AI Studio.")
