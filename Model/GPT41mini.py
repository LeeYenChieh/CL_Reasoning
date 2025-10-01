from openai import OpenAI
from Model.Model import Model
import os

class GPT41mini(Model):
    NAME = "GPT 4.1 mini"

    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = GPT41mini.NAME
        self.modelName = "gpt-4.1-mini-2025-04-14"
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def getRes(self, prompt) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0
            )
            return response.choices[0].message.content
        except:
            return ""
