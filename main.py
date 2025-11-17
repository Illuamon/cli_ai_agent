import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    prompt = sys.argv
    
    if len(prompt) <= 1:
        sys.exit("Error: no prompt")
    
    else:
        load_dotenv()
        apikey = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=apikey)
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt[1])
        print(response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
