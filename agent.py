from openai import OpenAI
import tomllib
import os
from dotenv import load_dotenv
from prompt import build_system_prompt
from tools import *
import json
import re


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

user = "Compare NVIDIA, AMD, Intel"
scratchpad = f"user: {user}\n\n"


def react_agent(current_scratchpad):

    response = client.chat.completions.create(
        model=model['name'],
        messages=[
            {"role":"system", "content": build_system_prompt()},
            {"role":"user", "content": current_scratchpad}
        ]
    )

    print(response)
    
    for line in response.choices[0].message.content.split('\n'):

        if line.startswith("Thought:"):
            current_scratchpad = current_scratchpad + line + "\n"
        elif line.startswith("Action:"):
            tools = {
                "web_search": web_search,
                "fetch_page": fetch_page
            }

            tool_name = re.split(r'\s*Action:\s*|\s*\(\s*|\s*\)\s*', line)[1]
            parameter = re.split(r'\s*Action:\s*|\s*\(\s*|\s*\)\s*', line)[2]

            current_scratchpad = current_scratchpad + "Action: " + tool_name + "\nAction Input: " + parameter + "\n"
            current_scratchpad = current_scratchpad + "Observations:" + str(tools[tool_name](parameter)) + "\n\n"

    if response.choices[0].message.content.__contains__("Final Answer:"):
        final_answer = response.choices[0].message.content.split("Final Answer: ")[1]
        current_scratchpad = current_scratchpad + "Final Answer: " + final_answer + "\n\n"

    return current_scratchpad, response.choices[0].message.content


count = 1
while count <= config["MAX_LOOP"]:
    
    scratchpad += f"TURN {count}\n"

    if count == config["MAX_LOOP"]:
        scratchpad += "You have reached the maximum number of research steps. \
            You MUST now issue your Final Answer using what you have gathered \
            so far.\n\n"

    scratchpad, response = react_agent(scratchpad)

    count += 1
    if response.__contains__("Final Answer:"):
        break

print(scratchpad)

   

