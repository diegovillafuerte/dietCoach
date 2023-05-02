from openai_api import chat_with_gpt

def get_calories(api_key, food_description):
    prompt = [{"role": "system", "content": "You are a caloric calculator, The user will give a description of a meal and you will reply with its nutritional information"},
                {"role": "user", "content": "How Many calories does a a salad that consist of two cups of lettuce, one large serving spoon of hummus, and a cup of grilled chicken breast have. Reply with the your best estimate of its nutritional values for calories, carbohydrates, protein, fat and sodium in a JSON format with no text outside of the JSON."},
                {"role": "assistant", "content": '{"calories": 375,"protein": 38,"carbohydrates": 25,"fat": 12,"sodium": 480}'}]
    prompt.append({"role": "user", "content": f"How many calories are in {food_description}. Reply with the your best estimate of its nutritional values for calories, carbohydrates, protein, fat and sodium in a
