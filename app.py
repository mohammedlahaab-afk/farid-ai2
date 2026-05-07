import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="آدم 777", page_icon="🧠")

# فتح الخزانة
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("الخزانة فارغة يا سيمي!")
    st.stop()

# عرض نسخة المكتبة للتأكيد
import google.generativeai as gai
st.caption(f"نسخة المكتبة: {gai.__version__}")

# الهيكل الجديد لـ "آدم" - متوافق تماماً مع 0.7.2
# لاحظي: أزلنا أي إشارة لـ v1beta وتركنا المكتبة تختار المسار الأفضل
@st.cache_resource
def init_adam():
    return genai.GenerativeModel('gemini-1.5-flash')

model = init_adam()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.markdown("### آدم (777) مستعد أخيراً")

# عرض المحادثة
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# التفاعل
if prompt := st.chat_input("تحدثي معه الآن..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # الطريقة الحديثة للإرسال دون تعقيدات
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        # إذا ظهر خطأ 429 (زحام)، سنخبرك بوضوح
        if "429" in str(e):
            st.warning("آدم مستيقظ، لكنه يحتاج ثوانٍ ليرد (ضغط حصة).")
        else:
            st.error(f"تنبيه: {e}")
