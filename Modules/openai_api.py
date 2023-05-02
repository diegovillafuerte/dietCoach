import openai

def chat_with_gpt(api_key, prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt)
    return response['choices'][0]['message']['content']
