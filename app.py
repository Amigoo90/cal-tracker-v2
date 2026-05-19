import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="حاسبة السعرات الذكية", layout="centered")

# محاولة جلب المفتاح وتفعيله
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("يرجى وضع GOOGLE_API_KEY في إعدادات Secrets")
except Exception as e:
    st.error(f"خطأ في إعداد المفتاح: {e}")

st.title("🍎 حاسبة السعرات الحرارية الذكية")
st.write("ارفع صورة وجبتك لتحليلها فوراً")

uploaded_file = st.file_uploader("اختر صورة الوجبة...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الوجبة المرفوعة', use_container_width=True)
    
    if st.button("تحليل الوجبة"):
        with st.spinner('يتم الآن تحليل الصورة...'):
            try:
                # تم تعديل السطر بالأسفل لضمان عمل الموديل
                model = genai.GenerativeModel('gemini-1.5-flash-latest') 
                response = model.generate_content([
                    "حلل مكونات هذه الوجبة بدقة. أعطني قائمة بالمكونات، السعرات الحرارية، والبروتين. ثم قدم نصيحة لزيادة الوزن.", 
                    image
                ])
                st.success("تم التحليل بنجاح:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء التحليل: {e}")
