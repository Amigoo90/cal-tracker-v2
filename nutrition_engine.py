import json
import os
import google.generativeai as genai

# إعداد مفتاح الـ API
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def analyze_food_image(image_path):
    # تم تغيير اسم النموذج هنا ليصبح gemini-1.5-flash ليعمل بدون أخطاء
    # جرب هذا الاسم أولاً (الأكثر استقراراً)
    model = genai.GenerativeModel('gemini-1.0-pro')
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    prompt = """
    請分析這張食物圖片，列出所有食物項目，並估計每種食物的重量 (g) 與卡路里 (kcal)。
    請嚴格依照以下 JSON 格式回傳，不要包含其他文字：
    [
        {"name": "食物名稱", "quantity_g": 0.0, "calories": 0}
    ]
    """
    response = model.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": image_data}
    ])
    
    json_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(json_text)

def calculate_tdee(weight_kg, height_cm, age, gender, activity_level=1.2):
    if gender == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return bmr * activity_level

def format_nutrition_result(items):
    total_calories = sum(item['calories'] for item in items)
    result = {
        "items": items,
        "total_calories": total_calories
    }
    return result
