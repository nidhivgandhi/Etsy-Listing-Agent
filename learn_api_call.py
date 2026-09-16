from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GENAI_API_KEY"])

response =client.models.generate_content(
    model = "gemini-3.6-flash",
    contents = "Say hello world in 5 different languages."
)
print(response.text)