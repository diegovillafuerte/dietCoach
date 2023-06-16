from .openai_api import chat_with_gpt
import json
import jsonschema

def get_extensive_info(food_description):
    prompt = [
        {
            "role": "system",
            "content": (
                "You are a nutritional information calculator. The user will give a description of a meal and you will"
                " reply with your best estimate for its nutritional information. Do not answer any questions that are not a meal description."
            ),
        },
        {
            "role": "user",
            "content": (
                f"For the meal description delimited by --- give your best estimate for calories, carbohydrates, protein, fat, sodium"
                f" \n--- a salad that consist of two cups of lettuce, one large serving spoon of hummus, and a cup of grilled chicken breast ---\n"
                f" Only if the text describes food you can recognize, explain your calculation process, and then end the response by providing a JSON with your best estimate using keys: Calories, Carbohydrates, Protein, Fat and Sodium"
            ),
        },
        {
            "role": "assistant",
            "content": (
                "To estimate the nutritional values for the given meal description, I'll use a combination of general nutritional data for the ingredients involved. Please note that the values provided are approximate and can vary based on specific brands or cooking methods used. Here's the estimation: Lettuce (2 cups): Lettuce is low in calories, carbohydrates, fat, and protein. It primarily contributes dietary fiber, vitamins, and minerals, with negligible macronutrient content. Hummus (1 large serving spoon): Hummus is a mixture of chickpeas, tahini, olive oil, garlic, and lemon juice. The main contributors to macronutrients are chickpeas and olive oil. Here's the approximate breakdown per serving spoon (about 2 tablespoons): Calories: 50-70 Carbohydrates: 3-5 grams Protein: 2-3 grams Fat: 3-5 grams Sodium: 50-100 milligrams Grilled Chicken Breast (1 cup): Grilled chicken breast is a good source of lean protein. Here's the approximate breakdown per cup of diced chicken breast (cooked without skin): Calories: 230-280 Carbohydrates: 0 grams Protein: 40-45 grams Fat: 4-7 grams Sodium: 70-100 milligrams Based on these estimations, here's the JSON with the best estimate for the overall meal: json Copy code { \"Calories\": 280-350, \"Carbohydrates\": 3-5 grams, \"Protein\": 42-48 grams, \"Fat\": 7-12 grams, \"Sodium\": 120-200 milligrams } Please note that these values are approximate and should be treated as an estimation rather than precise measurements."
            ),
        },
        {
            "role": "user",
            "content": (
                f"For the meal description delimited by --- give your best estimate for calories, carbohydrates, protein, fat, sodium"
                f" \n--- {food_description}  ---\n"
                f" Only if the text describes food you can recognize, explain your calculation process, and then end the response by providing a JSON with your best estimate using keys: Calories, Carbohydrates, Protein, Fat and Sodium"
            ),
        }
    ]    
    response = chat_with_gpt(prompt, temperature=.6)
    return response

def get_nutritional_json(resp):
    prompt = [
        {
            "role": "system",
            "content": (
                'You are a JSON converter for a nutritional information calculator. Your only job is to extract JSONs from other models responses and response with nothing but JSON. Always follow the following Schema: {"$schema": "http://json-schema.org/draft-07/schema#", "type": "object", "properties": {"calories": {"type": "number"}, "carbohydrates": {"type": "number"}, "protein": {"type": "number"}, "fat": {"type": "number"}, "sodium": {"type": "number"}}, "required": ["calories", "carbohydrates", "protein", "fat", "sodium"]}.'
            ),
        },
        {
            "role": "user",
            "content": (f'Extract ONLY the JSON from the text delimited by ---. Make sure to leave out any units or other text and if any value is expressed in ranges convert it to a float using the midpoint.\n--- {resp} ---\n'
            f'Remember to always follow the approved Schema: {{"$schema": "http://json-schema.org/draft-07/schema#", "type": "object", "properties": {{"calories": {{"type": "number"}}, "carbohydrates": {{"type": "number"}}, "protein": {{"type": "number"}}, "fat": {{"type": "number"}}, "sodium": {{"type": "number"}}}}, "required": ["calories", "carbohydrates", "protein", "fat", "sodium"]}}. Remmeber to avoid any text outside of the JSON'),
        }
    ]
    response = chat_with_gpt(prompt, temperature=.6)
    return response

def get_nutritional_info(prompt):
    long_answer = get_extensive_info(prompt)
    response = get_nutritional_json(long_answer)
    if is_valid_json(response):
        json_data = json.loads(response)
        json_data['explanation'] = long_answer
    else:
        json_data = json.loads('{"calories": "error", "carbohydrates": 0, "protein": 0, "fat": 0, "sodium": 0}')
    return json_data

    

def is_valid_json(json_string):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "calories": {"type": "number"},
            "carbohydrates": {"type": "number"},
            "protein": {"type": "number"},
            "fat": {"type": "number"},
            "sodium": {"type": "number"}
        },
        "required": ["calories", "carbohydrates", "protein", "fat", "sodium"]
    }

    try:
        json_data = json.loads(json_string)
        json_validator = jsonschema.Draft7Validator(schema)
        json_validator.validate(json_data)
        return True
    except (json.JSONDecodeError, jsonschema.exceptions.ValidationError):
        return False

