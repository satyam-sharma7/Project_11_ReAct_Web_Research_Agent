from openai import OpenAI
import tomllib
import os
from dotenv import load_dotenv
from prompt import Tools, Check_Final_Answer
from tools import *
import json

# Load env variables
load_dotenv()

# get toml config file
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# use selected LLM model
model = config["models"][config['MODEL']]

client = OpenAI(
    base_url = model['url'],
    api_key = os.getenv(model['api'])
)

user = "Who was bharat tiwari."
scratchpad = f"user: {user}\n\n"


print(scratchpad)

def select_tool(current_scratchpad):

    response = client.chat.completions.create(
        model=model['name'],
        messages=[
            {"role":"system", "content": Tools},
            {"role":"user", "content": current_scratchpad}
        ],
        response_format={"type": "json_object"}
    )

    print(response)
    response = json.loads(response.choices[0].message.content)
    current_scratchpad += f"Action: {response['tool']}\nAction Input: {response['parameters'][0]}\n"

    return response['tool'], response['parameters']


def use_tool(current_scratchpad):
    actions = {
        'web_search': web_search,
        'fetch_page': fetch_page
    }

    # select function to call
    tool_name, parameters = select_tool(scratchpad)
    print(tool_name)
    print(parameters)
    
    # call function
    tool_result = actions[tool_name](parameters[0])
    current_scratchpad += f"Observations: {tool_result}"
    
    return current_scratchpad


def is_final_answer(current_scratchpad):
        
    response = client.chat.completions.create(
        model=model['name'],
        messages=[
            {"role":"system", "content": Check_Final_Answer},
            {"role":"user", "content": current_scratchpad}
        ],
        response_format={"type": "json_object"}
    )
    
    response = json.loads(response.choices[0].message.content)

    return response['Final'], response['next_topic']


def reply(current_scratchpad):

    current_scratchpad = use_tool(current_scratchpad)

    is_relevent_info, next_topic = is_final_answer(current_scratchpad)
    if is_relevent_info == "no":
        current_scratchpad += f"Thought: I should dig deeper on title {next_topic} to find more information."


    print(current_scratchpad)

    return current_scratchpad

