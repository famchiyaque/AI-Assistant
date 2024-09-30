from openai import OpenAI
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{prompt}"}],
    )
    if response.choices:
        print(response.choices[0].message['content'])

inp = input("what's your prompt?: ")
get_response(inp)