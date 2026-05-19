import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="حاسبة السعرات الذكية", layout="centered")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets")

st.title("🍎 حاسبة السعرات")

uploaded_file = st.file_uploader("ارفع صورة وجبتك...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("تحليل الوجبة"):
        with st.spinner('جاري التحليل...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(["حلل الصورة: اذكر المكونات، السعرات، والبروتين.", image])
                st.success("النتيجة:")
                st.write(response.text)
            except Exception as e:
                st.error(f"خطأ: {e}")

