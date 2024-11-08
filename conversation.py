from openai import OpenAI
from dotenv import load_dotenv
from context_processor import ContextProcessor
import os
import re

class Conversation:
  def __init__(self, context_file, attempt_limit=10):

    # config paramaters
    self.attempt_limit = attempt_limit
    self.context_file = context_file

    # session paramaters
    self.messages = []
    self.attempt = 0
    self.session_credits = 0

    self.message_history = {}
    
    # initalise conversation
    self.client = self.initiaise_connection()
    self.context = self.generate_context() # context object

    
  @staticmethod
  def initiaise_connection():
    load_dotenv()
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

  @staticmethod
  def get_command(text) -> dict:
    # returns a dictionary of message and command, if command is not found return message and None
    try:
      pattern = r'```python([\s\S]*?)```|```([\s\S]*?)```'
      match = re.search(pattern, text, re.DOTALL)
      if match:
        command = match.group(1) or match.group(2)
        message = text.replace(match.group(0), "").strip()
      else:
        command = None
        message = text
    except Exception as e:
      print(e)
      command = None
      message = text
    return {"message": message, "command": command}
  
  def generate_context(self):
    context = ContextProcessor(self.context_file)
    return context

  def send_message(self, message) -> None:
    # Append the new message to the list of messages
    self.messages.append(message)

    # Append the message to the message history dictionary
    self.message_history[len(self.messages) - 1] = (

      {
        "role": message["role"],
        "content": message["content"],
        "command": None,
        "metadata":
          {
            "session_credits": self.session_credits,
            "attempt_number": self.attempt
          }
      }

    )
    
    # Generate a completion using the OpenAI API
    completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=self.messages
    )

    # Update the total session credits with the number of tokens used in the completion
    self.session_credits += completion.usage.total_tokens
    
    # Append the assistant's response to the list of messages
    self.messages.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content
        }
    )

    # Append the assistant's respoise to the message history dictionary
    self.message_history[len(self.messages) - 1] = (
      {
      "role": "assistant",
      "content":self.get_command(completion.choices[0].message.content)['message'],
      "command": self.get_command(completion.choices[0].message.content)["command"],
      "metadata":
        {
        "session_credits": self.session_credits,
        "attempt_number": self.attempt
        }
      }
    )
    

    