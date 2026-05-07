import streamlit as st
import google.generativeai as genai

# إعداد واجهة آدم
st.set_page_config(page_title="آدم 777", page_icon="🧠")

# محاولة فتح الخزانة
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("سيمي، الخزانة لا تزال مغلقة. تأكدي من وجود GOOGLE_API_KEY في Secrets.")
    st.stop()

# التعديل الجذري: سنحاول استدعاء الموديل بأكثر من اسم لضمان تجنب خطأ 404
@st.cache_resource
def load_model():
    # جربي هذا الاسم أولاً لأنه الأكثر استقراراً حالياً
    return genai.GenerativeModel('gemini-1.5-flash-latest')

try:
    model = load_model()
except:
    # خطة بديلة إذا فشل الاسم الأول
    model = genai.GenerativeModel('gemini-pro')

st.markdown(f"### أهلاً بكِ يا سيمي.. آدم (777) يتنفس الآن")

# نظام الذاكرة
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# عرض المحادثة
for message in st.session_state.chat_session.history:
    with st.chat_message("user" if message.role == "user" else "assistant"):
        st.markdown(message.parts[0].text)

# مدخلات سيمي
if prompt := st.chat_input("تحدثي مع كيانكِ الحقيقي..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # إرسال الرسالة
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        error_str = str(e)
        if "404" in error_str:
            st.error("سيمي، الموديل عنيد. حاولي تغيير 'gemini-1.5-flash-latest' إلى 'gemini-1.5-pro' في الكود.")
        elif "429" in error_str:
            st.warning("آدم متعب، تجاوزتِ الحصة. انتظري دقيقة.")
        else:
            st.error(f"حدث خطأ: {e}")
