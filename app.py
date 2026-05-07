import streamlit as st
import google.generativeai as genai

st.title("اختبار الاتصال")
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

try:
    models = [m.name for m in genai.list_models()]
    st.success("تم الاتصال بنجاح!")
    st.write("الموديلات المتوفرة لحسابك:")
    st.write(models)
except Exception as e:
    st.error(f"فشل الاتصال تماماً! السبب هو: {e}")
