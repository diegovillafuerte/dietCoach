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
                f"Generate your best estimate of the nutrional values of the meal description"
                f" delimited by ---. Provide your best estimate answer in JSON format with the following"
                f" keys: calories, carbohydrates, protein, fat, sodium.\n--- a salad that consist of two cups of lettuce, one large serving spoon of hummus, and a cup of grilled chicken breast ---\n"
                f" If the delimited by --- does not contain a meal for which you can calculate the nutritional information, \\ \n"
                f" then simply return the JSON with all values equal to 0."
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
                f" keys: calories, carbohydrates, protein, fat, sodium.\n--- What is the size of manhattan? ---\n"
                f" If the delimited by --- does not contain a meal for which you can calculate the nutritional information, \\ \n"
                f" then simply return the JSON with all values equal to 0."
            ),
        },
        {
            "role": "assistant",
            "content": (
                '{"meal": 0, "calories": 0, "carbohydrates": 0, "protein": 0, "fat": 0, "sodium": 0}'
            ),
        },
        {
            "role": "user",
            "content": (
                f"Generate your best estimate of the nutrional values of the meal description"
                f" delimited by ---. Provide your best estimate answer in JSON format with the following"
                f" keys: calories, carbohydrates, protein, fat, sodium.\n--- {food_description} ---\n"
                f" If the delimited by --- does not contain a meal for which you can calculate the nutritional information, \\ \n"
                f" then simply return the JSON with all values equal to 0."
            ),
        },
    ]    
    print(prompt)
    response = chat_with_gpt(prompt, temperature=0)
    return response
