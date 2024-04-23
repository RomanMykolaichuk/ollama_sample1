import os
from dotenv import load_dotenv
from groq import Groq
import json
import requests
import gradio as gr


# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("No API Key found in environment variables")
else: print("Ok")

client = Groq(api_key=api_key)

MODEL = 'llama3-8b-8192'


def get_game_score(team_name):
    """Get the current score for a given NBA game by querying the Flask API."""
    url = f'http://127.0.0.1:5000/score?team={team_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return json.dumps({"error": "API request failed", "status_code": response.status_code})

def run_conversation(user_prompt):
    # Step 1: send the conversation and available functions to the model
    messages=[
        {
            "role": "system",
            "content": "You are a function calling LLM that uses the data extracted from the get_game_score function to answer questions around NBA game scores. Include the team and their opponent in your response."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_game_score",
                "description": "Get the score for a given NBA game",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team_name": {
                            "type": "string",
                            "description": "The name of the NBA team (e.g. 'Golden State Warriors')",
                        }
                    },
                    "required": ["team_name"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",  
        max_tokens=4096
    )

    response_message = response.choices[0].message
    print(f"response_message: {response_message}")
    tool_calls = response_message.tool_calls
    print(f"tool_calls: {tool_calls}")
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_game_score": get_game_score,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                team_name=function_args.get("team_name")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )  # get a new response from the model where it can see the function response
        print(messages)
        return second_response.choices[0].message.content
    
def gradio_interface(user_prompt):
    return run_conversation(user_prompt)

interface=gr.Interface(fn=gradio_interface, inputs="text", outputs="text")
interface.launch()