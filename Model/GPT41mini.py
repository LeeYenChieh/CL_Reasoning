from openai import OpenAI
from Model.Model import Model
from api_key import gpt_api_key

class GPT41mini(Model):
    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = "GPT 4.1 mini"
        self.modelName = "gpt-4.1-mini-2025-04-14"
        self.client = OpenAI(api_key=gpt_apt_key)
    
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
