from openai import OpenAI
from time import time
from dotenv import load_dotenv

import pandas as pd
import logging
import re
import os

logger = logging.getLogger(__name__)
load_dotenv()

def extract_code_block(text):
    pattern = r"```python(.*?)```"
    code_block = re.search(pattern, text, re.DOTALL)
    if code_block:
        return code_block.group(1)
    else:
        return "No code block found"


messages = []
total_credits_used = 0


class Conversation():
  def __init__(self, context):

    # meta data
    self.total_session_credits = 0
    self.response = None
    self.messages = []
    
    self.context = context
    self.client = self.initiaise_connection()
    self.process_context()
    
  @staticmethod
  def initiaise_connection():
    return OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

  def process_context(self):
    self.messages.append(
      {
        "role": "system", 
        "content":
            f"""
              You are my Personal Analyst, take this csv "PremierLeague.csv"', and its columns {self.context.dtypes}.
              First introduce yourself, then give me a brief description on what this csv represents.
              Then suggest 3 graphs I could make to understand the dataset.

              When ever you reply after your first meessage, you will always give some conversational response and also python code I could
              excute to produce this graph, your code must assume you need to import the csv from the data/ directory using pandas then make a plot with it, 
              this code must always be wrapped within ``` ``` so I can copy and paste it.
            """
      }
    )
    
    completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=self.messages
    )

    # append to message list
    self.messages.append(
      {
        "role": "assistant", 
        "content": completion.choices[0].message.content
      }
    )
    #update total_credits
    self.total_session_credits += completion.usage.total_tokens
    # get reponse in json
    self.response = {
      "message": completion.choices[0].message.content,
      "command": extract_code_block(completion.choices[0].message.content)
    }

    self.print_message()


  def send_message(self):
    # get message
    self.messages.append({"role": "user", "content": input(f"message: \n")})

    # get completion of conversation
    completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=self.messages
    )
    # append to message list
    self.messages.append(
      {
        "role": "assistant", 
        "content": completion.choices[0].message.content
      }
    )
    #update total_credits
    self.total_session_credits += completion.usage.total_tokens
    # get reponse in json
    self.response = {
      "message": completion.choices[0].message.content,
      "command": extract_code_block(completion.choices[0].message.content)
    }

  def execute_code(self):
    # print("-"*15)
    # print(f'EXECUTING CODE: \n {self.response["command"]}')
    # print("-"*15)
    try:
      exec(self.response["command"])
    except Exception as e:
      print(e)

  # prints the latest message
  def print_message(self):
    print(self.response["message"])


if __name__ == '__main__':

  df = pd.read_csv('data/PremierLeague.csv')

  conversation = Conversation(
    context = df
  )
  
  while True:  
    conversation.send_message()
    conversation.print_message()
    conversation.execute_code()
