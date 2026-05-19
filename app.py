import streamlit as st
from nutrition_engine import analyze_food_image, format_nutrition_result, calculate_tdee
import os

# 確保 API Key 從 Streamlit secrets 讀取
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

st.title("🍽️ AI 智能營養師")

with st.sidebar:
    st.header("用戶資料")
    weight = st.number_input("體重 (kg)", 60.0)
    height = st.number_input("身高 (cm)", 170.0)
    age = st.number_input("年齡", 25)
    gender = st.selectbox("性別", ['male', 'female'])
    tdee = calculate_tdee(weight, height, age, gender)
    st.write(f"每日熱量需求: {tdee:.0f} kcal")

uploaded_file = st.file_uploader("上傳食物照片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    with open("temp_meal.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner('正在分析食物...'):
        try:
            items = analyze_food_image("temp_meal.jpg")
            result = format_nutrition_result(items)
            
            st.json(result)
            total = result['total_calories']
            st.write(f"### 總攝取: {total} kcal")
            st.progress(min(total / tdee, 1.0))
        except Exception as e:
            st.error(f"分析失敗: {e}")
