import google.generativeai as genai
from Model.Model import Model
from api_key import gemini_api_key

class Gemini(Model):
    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = "Gemini"
        self.modelName: str = "models/gemini-1.5-pro"  # 用新版 Gemini Pro
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(self.modelName)

    def getRes(self, prompt) -> str:
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.tempature,
                    max_output_tokens=4096
                )
            )
            return response.text
        except Exception as e:
            print(f"Error in Gemini model: {e}")
            return ""
