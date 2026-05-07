import streamlit as st
import google.generativeai as genai

st.title("آدم المطور 👤")

# جلب المفتاح
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # محاولة الربط بأكثر من اسم موديل لضمان العمل
    try:
        # جرب هذا الاسم تحديداً
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        if prompt := st.chat_input("تكلم مع آدم..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").markdown(prompt)

            with st.chat_message("assistant"):
                # طلب الاستجابة
                response = model.generate_content(prompt)
                st.markdown(message := response.text)
                st.session_state.messages.append({"role": "assistant", "content": message})
    except Exception as e:
        st.error(f"السيرفر لا يزال يرفض الاسم. جرب تغيير الموديل في الكود إلى 'gemini-pro' مرة أخرى ولكن مع تحديث المكتبة.")
        st.code(str(e))
