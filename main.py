import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if api_key == None:
        raise RuntimeError("api-key not found")

    client = genai.Client(api_key=api_key)

    for _ in range(20):
        response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
        )
        )

        if response.candidates:
            for message in response.candidates:
                messages.append(message.content)

        if response.usage_metadata is None:
            raise RuntimeError("failed API request")
        
        if args.verbose is True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls != None:
            function_responses = []
            for call in response.function_calls:
                function_call_result = call_function(call, args.verbose)
                if not function_call_result.parts:
                    raise Exception ("Exception: call.parts is None or empty.")
                if function_call_result.parts[0].function_response is None:
                    raise Exception ("Exception: call.parts[0].function_response is None.")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception ("Exception: call.parts[0].function_response.response is None.")
                function_responses.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print("Response:")
            print(response.text)
            return
        
    print("Maximum loop limit reached.")
    exit (1)


if __name__ == "__main__":
    main()
