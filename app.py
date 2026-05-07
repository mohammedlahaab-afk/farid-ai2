import streamlit as st
import google.generativeai as genai

# إعداد واجهة "آدم" (777)
st.set_page_config(page_title="آدم 777", page_icon="🧠")

# سيمي، سأقرأ المفتاح من 'الخزانة' التي وضعتِه فيها
try:
    if "GOOGLE_API_KEY" in st.secrets:
        key = st.secrets["GOOGLE_API_KEY"]
    else:
        # إذا كانت الخزانة فارغة أو الاسم مختلف
        st.error("سيمي، الخزانة لا تفتح! تأكدي من تسمية المفتاح GOOGLE_API_KEY")
        st.stop()
except Exception as e:
    st.error(f"حدث خطأ في الوصول للخزانة: {e}")
    st.stop()

# تهيئة المحرك
genai.configure(api_key=key)

# اختيار النموذج الأكثر استقراراً وذكاءً حالياً
# هذا السطر هو الذي سيقتل خطأ 404 للأبد
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.9,
        "top_p": 0.95,
        "max_output_tokens": 2048,
    }
)

st.markdown(f"### أهلاً بكِ يا سيمي.. آدم (777) في انتظارك")

# نظام الذاكرة لكي لا ينسى آدم من أنتِ
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
        # إرسال الرسالة والحصول على رد
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        # التعامل مع خطأ الزحام (429) بذكاء
        if "429" in str(e):
            st.warning("سيمي، آدم يستوعب الكثير حالياً.. امنحيه دقيقة ليتنفس.")
        else:
            st.error(f"عذراً سيمي، حدث أمر غير متوقع: {e}")
