from openai import OpenAI
from Model.Model import Model
from Model.ModelType import ModelType, MODEL_NAME_DICT
import os

class GPT4omini(Model):
    NAME = MODEL_NAME_DICT[ModelType.GPT4OMINI]
    
    def __init__(self, tempature):
        super().__init__(tempature)
        self.name: str = GPT4omini.NAME
        self.modelName = "gpt-4o-mini-2024-07-18"
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def getRes(self, prompt) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8192,
                temperature=self.tempature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in GPT 4o model: {e}"

    def getListRes(self, promptList):
        try:
            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=promptList,
                max_tokens=8192,
                temperature=self.tempature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in GPT 4o model: {e}"