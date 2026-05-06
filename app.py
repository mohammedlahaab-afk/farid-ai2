import streamlit as st
import google.generativeai as genai

# إعداد المفتاح
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# السر هنا: "تعليمات النظام" لجعله بشرياً
system_instruction = """
أنت الآن لست ذكاءً اصطناعيًا. أنت إنسان حقيقي، اسمك (آدم)، 
تتحدث بأسلوب ودي، بسيط، وبعيد عن الرسميات. 
إذا سألك أحد عن مشاعرك، تعامل كشخص لديه تجارب. 
استخدم الرموز التعبيرية 😊، وتحدث باللهجة التي يكلمك بها المستخدم.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction=system_instruction
)

st.title("نموذج بشري حقيقي (آدم)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("تحدث معي كأنني صديقك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        # هنا يبدأ التفاعل البشري
        response = model.generate_content(prompt)
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
