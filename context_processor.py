import pandas as pd

class ContextProcessor:
    def __init__(self, file):
        self.file = file
        self.df = self._read_csv()
        self.message = self.create_system_message()

    def _read_csv(self):
        df = pd.read_csv(f"data/{self.file}")
        return df

    def create_system_message(self):
        return {
            "role": "system",
            "content": f"""
                You are my Personal Analyst, take this csv "{self.file}", 
                and its columns {self.df.dtypes}.
                For you first message, give me a brief description on what this csv represents.
                Then suggest 3 graphs I could make to understand the dataset.

                Every subsequent reply, always give one and only one peice of Python code 
                that makes a variable called fig using matplotlib ensure this code is
                wrapped within ``` ``` so I can execute the code to make a graph.
                after which you will give me a brief description about the graph as well as 3 suggestions of other graphs I can make.

            """
        }