from openai import OpenAI
from Model.Model import Model
import os

class QWEN(Model):
    NAME = "QWEN 3-8b"
    
    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = QWEN.NAME
        self.modelName = "qwen3-8b"
        self.client = OpenAI(
            api_key=os.getenv("QWEN_API_KEY"),
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
    
    def getRes(self, prompt) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.modelName,
                extra_body={"enable_thinking": False},
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8192,
                temperature=self.tempature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in QWEN model: {e}"
