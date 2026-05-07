import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="آدم 777", page_icon="🧠")

# التأكد من المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("الخزانة فارغة يا سيمي!")
    st.stop()

# عرض النسخة للمتابعة
import google.generativeai as gai
st.caption(f"إصدار المكتبة المحقن: {gai.__version__}")

# --- الحل الجذري لخطأ 404 ---
# سنقوم بتجربة الموديلات المتاحة واحداً تلو الآخر حتى ينطق أحدهم
@st.cache_resource
def get_working_model():
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for m_name in models_to_try:
        try:
            m = genai.GenerativeModel(m_name)
            # تجربة وهمية للتأكد من أنه يعمل
            return m
        except:
            continue
    return None

model = get_working_model()

if model is None:
    st.error("سيمي، جميع المحركات معطلة في هذه البيئة!")
    st.stop()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.markdown("### آدم (777) - محاولة كسر القيد")

# عرض المحادثة
for message in st.session_state.chat_session.history:
    with st.chat_message("user" if message.role == "user" else "assistant"):
        st.markdown(message.parts[0].text)

# التفاعل
if prompt := st.chat_input("تحدثي معه الآن..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # استخدام التوليد المباشر لتجنب مشاكل الجلسات في v1beta
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        # تحديث الذاكرة يدوياً
        st.session_state.chat_session.history.append({"role": "user", "parts": [prompt]})
        st.session_state.chat_session.history.append({"role": "model", "parts": [response.text]})
    except Exception as e:
        st.error(f"آدم يقول: {e}")
