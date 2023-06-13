import openai
import os
import sys

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    sys.exit("Error: OPENAI_API_KEY environment variable not set.")

def chat_with_gpt(prompt, model="gpt-3.5-turbo", temperature=.6):
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=temperature)
    return response.choices[0].message["content"]