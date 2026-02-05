import openai
from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

# Load API keys from environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Define the model - GPT-3/4 or GPT-Neo/GPT-J via Hugging Face
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B", use_auth_token=HUGGINGFACE_TOKEN)

# Function to generate code based on prompt
def generate_code(prompt: str, max_length=200):
    response = generator(prompt, max_length=max_length, num_return_sequences=1)
    return response[0]['generated_text']

# Example function call
if __name__ == "__main__":
    prompt = "Write a Python function to calculate the factorial of a number."
    generated_code = generate_code(prompt)
    print("Generated Code:\n", generated_code)