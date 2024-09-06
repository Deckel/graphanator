from openai import OpenAI
from time import time
from dotenv import load_dotenv
from matplotlib.pyplot import plot, draw, show
from custom_logger import CustomFormatter

import pandas as pd
import matplotlib.pyplot as plt
import signal
import sys
import logging
import re
import os

# create logger with '__name__'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

# take environment variables from .env
load_dotenv()

def sig_handler(signal_number, stack_frame):
    logger.error('Exiting script')
    plt.close("all")
    sys.exit(-1)

def seperate_cmd(text) -> dict:
  # returns a dictonary of message and command, if command is not found return message and None
    try:
      pattern = r'```python([\s\S]*?)```|```([\s\S]*?)```'
      response = re.sub(pattern, "", text)
      command = re.search(pattern, text, re.DOTALL).group(1)
      resp_dict = {
        "response": response,
        "command": command
      }
    except Exception as e:
      logger.warning(f"Could not find code block")
      resp_dict = {
        "response": text,
        "command": None
      }
    return resp_dict


class FileManager:
    @staticmethod
    def get_sorted_files(directory):
        files = [(file, os.path.getctime(os.path.join(directory, file))) for file in os.listdir(directory)]
        sorted_files = sorted(files, key=lambda x: x[1], reverse=True)
        return sorted_files
    
    @staticmethod
    def get_latest_file(directory):
        return FileManager.get_sorted_files(directory)[0]
    
class ContextProcessor:
    def __init__(self, context):
        self.context = context

    def create_initial_message(self):
        latest_file = FileManager.get_sorted_files(f"{os.getcwd()}/data")[0][0]
        return {
            "role": "system",
            "content": f"""
                You are my Personal Analyst, take this csv "{latest_file}", 
                and its columns {self.context.dtypes}.
                First introduce yourself, then give me a brief description on what this csv represents.
                Then suggest 3 graphs I could make to understand the dataset.

                Whenever you reply after your first message, you will always give some conversational response and also python code I could
                execute to produce this graph, your code must assume you need to import the csv from the data/ directory using pandas then make a plot with it, 
                this code must always be wrapped within ``` ``` so I can copy and paste it.
            """
        }


class Conversation():
  def __init__(self, context):

    # meta data
    self.total_session_credits = 0
    self.response = None
    self.messages = []
    self.attempt = 0
    self.attempt_limit = 4
    
    self.context = context
    self.client = self.initiaise_connection()
    self.context_processor = ContextProcessor(context)
    self.process_context()
    
  @staticmethod
  def initiaise_connection():
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

  def process_context(self):
    initial_message = self.context_processor.create_initial_message()
    self.messages.append(initial_message)
   
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
    self.response = completion.choices[0].message.content
    # log message
    logger.info(self.response)


  def message(self, role, message) -> None:
    # append message
    self.messages.append({"role": role, "content": message})
    
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
    # update reponse
    self.response = resp_dict = seperate_cmd(completion.choices[0].message.content)
    # log the response
    logger.info(self.response["response"])
  
  def execute_code(self):
    try:
      cmd = self.response["command"]
      # get rid of the plt.show() and replace it with plt.ion()
      cleaned_cmd = cmd.replace("plt.show()","plt.ion()\nplt.show()")
      plt.close()
      context = {}
      logger.debug("Executing Python...")
      exec(cleaned_cmd, context)
      self.attempt = 0
    except Exception as e:
      # itterate attempt counter
      self.attempt += 1
      # if max attempt reach reset conversation, otherwise retry
      if self.attempt == self.attempt_limit:
        logger.critical(f"Maximum attempts reached, resetting conversation to last message...")    
        self.messages = self.messages[:-(self.attempt+self.attempt_limit)]
        logger.info(self.messages[-1]["content"])
      else:
        logger.critical(f"Execution failed on attempt {self.attempt} with error: \n{e}")
        self.message('user', 'The code failed with the error please rewrite the code to fix it: {e}')
        logger.critical(f"Regenerating...")
        conversation.execute_code()

if __name__ == '__main__':
  signal.signal(signal.SIGINT, sig_handler)
  signal.signal(signal.SIGTSTP, sig_handler)
  # get path of latest file added to the folder data
  latest_file = FileManager.get_latest_file(f"{os.getcwd()}/data")[0]
  f_path = os.path.join('data', latest_file)
  df = pd.read_csv(f_path)

  conversation = Conversation(context=df)

  while True:
    # Message the bot
    user_input = input("message: \n")
    conversation.message('user', user_input)
    
    # If we found a command, execute it
    if conversation.response and conversation.response.get("command"):
        conversation.execute_code()
