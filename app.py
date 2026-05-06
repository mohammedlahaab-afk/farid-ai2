# كود تشخيصي لكشف سبب الخلل
try:
    if "MY_FREE_KEY" in st.secrets:
        api_key = st.secrets["MY_FREE_KEY"]
        if api_key.startswith("sk-"):
            st.warning("⚠️ تنبيه: أنت تستخدم مفتاح OpenAI وهو يتطلب رصيداً مدفوعاً.")
        elif api_key.startswith("gsk_"):
            st.success("✅ تم التعرف على مفتاح Groq المجاني.")
    else:
        st.error("❌ الخزنة (Secrets) فارغة تماماً، التطبيق لا يرى أي مفتاح.")
except Exception as e:
    st.error(f"حدث خطأ أثناء محاولة قراءة الخزنة: {e}")
