import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import call_function, available_functions
from config import MAX_ITERS

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    if len(sys.argv) < 2:
        print("Error, no prompt was provided after program name")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    # create new instance of Gemini AI client
    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(20): # agent stops eventually
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

    # else:
    #     print(response.text)
    #     break
    
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


    function_calls = response.function_calls
    if function_calls:
        # print(function_calls)
        for function_call_part in function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result = call_function(function_call_part)
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Fatal exception. No response from AI Agent")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(function_call_result)

    if not function_calls:
        raise Exception("no function responses generated, exiting.")
    


if __name__ == "__main__":
    main()




    
