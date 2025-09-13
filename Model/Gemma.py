import google.generativeai as genai
from Model.Model import Model
from api_key import gemini_api_key

class Gemma(Model):
    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = "Gemma"
        self.modelName = "models/gemma-3-27b-it"  # Using strongest Gemma model
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
            print(f"Error in Gemma model: {e}")
            return ""
