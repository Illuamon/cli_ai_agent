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
    
    iteration_no = 1

    #content generation
    while iteration_no <= 20:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=messages,
                config=types.GenerateContentConfig(
                        tools=[available_functions], system_instruction=system_prompt
                ),
            )

            candidates_list = response.candidates
            for can in candidates_list:
                messages.append(can.content)

            #calling the functions 
            function_calls = []

            for can in candidates_list:
                can_parts = can.content.parts
                for part in can_parts:
                    # is this part a function call?
                    if hasattr(part, "function_call") and part.function_call is not None:
                        function_calls.append(part.function_call)

            if verbose:
                print(f"[iter {iteration_no}] function calls found: {len(function_calls)}")
            
            function_response_list = []

            if not function_calls:
                pass
            else:
                for f in function_calls:
                    function_call_result = call_function(f, verbose)

                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("no function_response.response")
                    else:
                        function_response_list.append(function_call_result.parts[0])
                    
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
        
            
            if function_response_list:
                messages.append(types.Content(parts=function_response_list, role="user"))

            #finished???
            if not function_calls:
                # No tools requested this turn, so treat this as the final answer.
                if response.text:
                    print("Final response:")
                    print(response.text)
                else:
                    print("Final response had no text.")
                break

            iteration_no += 1

        except Exception as e:
            print(e)
            break

    if verbose:
        print(f"User prompt: {text_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
if __name__ == "__main__":
    main()
