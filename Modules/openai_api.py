import openai
import os

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    sys.exit("Error: OPENAI_API_KEY environment variable not set.")

def chat_with_gpt(prompt, key=api_key):
    openai.api_key = key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt)
    return response['choices'][0]['message']['content']
