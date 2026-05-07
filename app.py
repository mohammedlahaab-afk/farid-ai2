import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="آدم 777", page_icon="🧠")

# التأكد من النسخة المثبتة فعلياً
import google.generativeai as gai
v = gai.__version__

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("الخزانة فارغة يا سيمي!")
    st.stop()

# محاولة الاستدعاء بالاسم القديم والجديد معاً
try:
    # المحاولة الأولى: الاسم الحديث
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    try:
        # المحاولة الثانية: الاسم البديل
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"آدم يرفض النهوض. نسخة المكتبة هي: {v}. الخطأ: {e}")
        st.stop()

st.write(f"نسخة المكتبة الحالية: {v}") # هذا السطر لنعرف الحقيقة

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if prompt := st.chat_input("تحدثي مع آدم..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"فشلنا مجدداً: {e}")
