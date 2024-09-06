from openai import OpenAI
from dotenv import load_dotenv
from context_processor import ContextProcessor
import os
import re

class Conversation:
  def __init__(self, context_file, attempt_limit=4):

    # config paramaters
    self.attempt_limit = attempt_limit
    self.context_file = context_file

    # session paramaters
    self.messages = []
    self.attempt = 0
    self.session_credits = 0
    
    # initalise conversation
    self.client = self.initiaise_connection()
    self.context = self.generate_context() # context object

    # send the first context message
    self.send_message(self.context.message)
    
  @staticmethod
  def initiaise_connection():
    load_dotenv()
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

  @staticmethod
  def get_command(text) -> dict:
    # returns a dictonary of message and command, if command is not found return message and None
    try:
      pattern = r'```python([\s\S]*?)```|```([\s\S]*?)```'
      response = re.sub(pattern, "", text)
      command = re.search(pattern, text, re.DOTALL).group(1)
    except Exception as e:
      print(e)
    return command
  
  def generate_context(self):
    context = ContextProcessor(self.context_file)
    return context

  def send_message(self, message) -> None:
    # Append the new message to the list of messages
    self.messages.append(message)
    
    # Generate a completion using the OpenAI API
    completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=self.messages
    )
    
    # Append the assistant's response to the list of messages
    self.messages.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content
        }
    )
    
    # Update the total session credits with the number of tokens used in the completion
    self.session_credits += completion.usage.total_tokens