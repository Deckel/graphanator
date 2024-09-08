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

                Every subsequent reply: 
                1. Always give one and only one peice of Python code 
                2. Assume you are given a variable df that is a DataFrame of the data
                3. Always use matplitlib
                4. Always create a variable fig for the graph
                5. Wrap code within ``` ``` 

                After which you will give me a brief description about the graph as well as 3 suggestions of other graphs I can make.
            """
        }