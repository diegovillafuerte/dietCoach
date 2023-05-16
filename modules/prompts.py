from .openai_api import chat_with_gpt

def get_nutritional_info(food_description):
    prompt = [
        {
            "role": "system",
            "content": (
                "You are a caloric calculator. The user will give a description of a meal and you will"
                " reply with its nutritional information. Provide your best estimate answer in JSON"
                " format with the following keys: calories, carbohydrates, protein, fat, sodium."
            ),
        },
        {
            "role": "user",
            "content": (
                "Give me your best estimate of the nutrional values of a salad that consist of two cups"
                " of lettuce, one large serving spoon of hummus, and a cup of grilled chicken breast."
                " Provide your best estimate answer in JSON format with the following keys: calories,"
                " carbohydrates, protein, fat, sodium."
            ),
        },
        {
            "role": "assistant",
            "content": (
                '{"meal": "a salad that consist of two cups of lettuce, one large serving spoon'
                ' of hummus, and a cup of grilled chicken breast", "calories": 375, "carbohydrates": 25,'
                ' "protein": 38, "fat": 12, "sodium": 480}'
            ),
        },
        {
            "role": "user",
            "content": (
                f"Generate your best estimate of the nutrional values of the meal description"
                f" delimited by ---. Provide your best estimate answer in JSON format with the following"
                f" keys: calories, carbohydrates, protein, fat, sodium.\n---{food_description}---\n"
                f" If the delimited by --- does not contain a meal you can understand, \\ \n"
                f" then simply return the JSON with all values equal 0."
            ),
        },
    ]    
    print(prompt)
    response = chat_with_gpt(prompt, temperature=0)
    return response
