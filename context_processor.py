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
                First introduce yourself, then give me a brief description on what this csv represents.
                Then suggest 3 graphs I could make to understand the dataset.

                Whenever you reply, always give one and only one peice of Python code wrapped within ``` ``` that I can execute to make a graph, 
                after which you will give me a brief description about the graph as well as 3 suggestions of other graphs I can make.

            """
        }