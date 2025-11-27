import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_functions import available_functions
from prompts import system_prompt

def main():
    raw_args = sys.argv
    text_prompt = raw_args[1]

    if len(raw_args) <= 1:
        sys.exit("Error: no prompt")

    messages = [types.Content(role="user", parts=[types.Part(text=text_prompt)]),]    

    load_dotenv()
    apikey = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=apikey)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
        ),
    )

    function_call_part = response.function_calls

    if not function_call_part:
        print(response.text)
    else:
        for f in function_call_part:
            print(f"Calling function: {f.name}({f.args})")
    
    if "--verbose" in raw_args:
        print(f"User prompt: {text_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
