from openai import OpenAI
from time import time
import re



def extract_code_block(text):
    pattern = r"```python(.*?)```"
    code_block = re.search(pattern, text, re.DOTALL)
    if code_block:
        return code_block.group(1)
    else:
        return "No code block found"


messages = []
total_credits_used = 0


class MyPersonalAnalyst:
  def __init__(self):
    self.client = self.initiaise_connection()
    self.messages = {"role": "user", "content": input(f"Start a conversation: \n")}
    self.total_credits_use

  @staticmethod
  def initiaise_connection():
    return OpenAI(api_key = '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')

  def new_chat(self):
    self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=self.messages
    )




# while True:

#   client = OpenAI(api_key = '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')

#   # append prompt  
#   messages.append({"role": "user", "content": input(f"Start a conversation: \n")})

#   # send message
#   completion = client.chat.completions.create(
#       model="gpt-3.5-turbo",
#       messages=messages
#     )

#   # total_credits_used += completion.usage.total_tokens
#   # print(f"Total Credits used so far: {total_credits_used}")

#   # print reponse
#   print(completion.choices[0].message.content)

#   print(f"CODE BLOCK: \n {extract_code_block(completion.choices[0].message.content)}")

#   # execute any code
#   exec(extract_code_block(completion.choices[0].message.content))

#   # append response
#   messages.append({"role": "assistant", "content": completion.choices[0].message.content})


# if __name__ == '__main__':
  main()