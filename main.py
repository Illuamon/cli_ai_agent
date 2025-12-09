import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

def main():
    raw_args = sys.argv
    verbose = False

    if len(raw_args) <= 1:
        sys.exit("Error: no prompt")
    
    if "--verbose" in raw_args:
        verbose = True

    text_prompt = raw_args[1]
    messages = [types.Content(role="user", parts=[types.Part(text=text_prompt)]),]    

    load_dotenv()
    apikey = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=apikey)

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
        ),
    )

    function_call_part = response.function_calls
    function_response_list = []

    if not function_call_part:
        print(response.text)
    else:
        for f in function_call_part:
            function_call_result = call_function(f, verbose)

            if not function_call_result.parts[0].function_response.response:
                raise Exception("no function_response.response")
            else:
                function_response_list.append(function_call_result.parts[0])
            
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    if verbose:
        print(f"User prompt: {text_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
