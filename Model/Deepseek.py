from Model.Model import Model
from openai import OpenAI
import os

class Deepseek(Model):
    NAME = "Deepseek"

    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = Deepseek.NAME
        self.modelName = "deepseek-reasoner"
        self.client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com"
        )

    def getRes(self, prompt) -> str:
        print("Sending request to Deepseek...")
        print(f"Model: {self.modelName}")
        print(f"Prompt: {prompt[:100]}...")  # 只印前 100 字

        try:
            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096,
                temperature=self.tempature,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in Deepseek model: {e}")
            return ""

