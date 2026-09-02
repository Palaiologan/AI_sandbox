from dotenv import load_dotenv
import os
from openai import OpenAI

# load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print("API key loaded:", api_key)

# initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# actual API call
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {
            "role": "user",     # Note: " refers to the human request
            "content": "Explain APIs in terms that a 10-year old child can understand.  Can use metaphors or examples to illustrate."
        }
    ]
)

print(response.choices[0].message.content)