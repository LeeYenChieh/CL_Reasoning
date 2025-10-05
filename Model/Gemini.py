import google.generativeai as genai
from Model.Model import Model
import os

class Gemini(Model):
    NAME = "Gemini 2.5 Flash"

    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = Gemini.NAME
        self.modelName: str = "gemini-2.5-flash-lite"  # 用新版 Gemini Pro
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel(self.modelName)
        print(genai.list_models())

    def getRes(self, prompt) -> str:
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.tempature,
                    max_output_tokens=8192
                )
            )
            return response.text
        except Exception as e:
            return f"Error in Gemini model: {e}"
