import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد واجهة التطبيق
st.set_page_config(page_title="حاسبة السعرات الذكية", layout="centered")

# جلب المفتاح من Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("يرجى التأكد من وضع المفتاح في إعدادات Secrets")

st.title("🍎 حاسبة السعرات الحرارية الذكية")
st.write("ارفع صورة وجبتك لتحليلها فوراً")

uploaded_file = st.file_uploader("اختر صورة الوجبة...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الوجبة المرفوعة', use_container_width=True)
    
    if st.button("تحليل الوجبة"):
        with st.spinner('انتظر قليلاً...'):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(["حلل هذه الصورة وأعطني السعرات والبروتين لكل مكون.", image])
            st.success("نتائج التحليل:")
            st.write(response.text)
