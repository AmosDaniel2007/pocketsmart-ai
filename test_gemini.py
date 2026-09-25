from dotenv import load_dotenv
from google import genai

load_dotenv()

print("Starting test", flush=True)
client = genai.Client()

response = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="Say hello in one short sentence.",
)

print("Gemini replied:", repr(response.output_text), flush=True)