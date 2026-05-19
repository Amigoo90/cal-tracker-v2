import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="حاسبة السعرات الذكية", layout="centered")

# الربط بمفتاح API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("يرجى التأكد من إضافة GOOGLE_API_KEY في إعدادات Secrets")

st.title("🍎 حاسبة السعرات الحرارية الذكية")
st.write("ارفع صورة وجبتك لتحليلها فوراً وبدقة")

uploaded_file = st.file_uploader("اختر صورة الوجبة...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الوجبة المرفوعة', use_container_width=True)
    
    if st.button("تحليل الوجبة الآن"):
        with st.spinner('يتم الآن فحص الصورة واستخراج البيانات...'):
            try:
                # استخدمنا الاسم الأكثر استقراراً للموديل
                
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


 
                
                prompt = """
                أنت خبير تغذية ورياضة. حلل هذه الصورة بدقة:
                1. اذكر المكونات الموجودة.
                2. احسب السعرات الحرارية والبروتين لكل مكون.
                3. أعطِ نصيحة محددة لزيادة الوزن وبناء العضلات بناءً على هذه الوجبة.
                """
                
                response = model.generate_content([prompt, image])
                
                st.success("التحليل المكتمل:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ تقني: {e}")
                st.info("نصيحة: تأكد من أن مفتاح API الذي وضعته في Secrets فعال ولم يتجاوز حد الاستخدام اليومي.")
