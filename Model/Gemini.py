from openai import OpenAI
from Model.Model import Model
import os

class Gemini(Model):
    NAME = "Gemini 2.5 Flash"

    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = Gemini.NAME
        self.modelName: str = "gemini-2.5-flash-lite"  # 用新版 Gemini Pro
        self.client = OpenAI(
            api_key=os.getenv('GEMINI_API_KEY'),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def getRes(self, prompt) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8192,
                temperature=self.tempature,
                stream=False
            )

            return response.choices[0].message
        except Exception as e:
            return f"Error in Gemini model: {e}"
    
    def getListRes(self, promptList):
        try:
            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=promptList,
                max_tokens=8192,
                temperature=self.tempature,
                stream=False
            )

            return response.choices[0].message
        except Exception as e:
            return f"Error in Gemini model: {e}"