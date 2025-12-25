from enum import Enum

class ModelType(str, Enum):
    GPT41MINI = 'gpt4.1mini'
    GPT4OMINI = 'gpt4omini'
    DEEPSEEK = 'deepseek'
    GEMINI = 'gemini'
    GEMMA = 'gemma'
    QWEN = 'qwen'
    
MODEL_LIST = [m.value for m in ModelType]
MODEL_NAME_DICT = {
    ModelType.GPT41MINI.value: "GPT 4.1 mini",
    ModelType.GPT4OMINI.value: "GPT 4o mini",
    ModelType.DEEPSEEK.value: "Deepseek",
    ModelType.GEMINI.value: "Gemini 2.5 Flash",
    ModelType.GEMMA.value: "Gemma",
    ModelType.QWEN.value: "QWEN 3-8b"
}

def get_model_map():
    # ← 只有真正用到時才 import，不會循環
    from Model.GPT41mini import GPT41mini
    from Model.GPT4omini import GPT4omini
    from Model.Deepseek import Deepseek
    from Model.Gemini import Gemini
    from Model.QWEN import QWEN
    from Model.Gemma import Gemma
    return {
        "GPT 4.1 mini": GPT41mini,
        "GPT 4o mini": GPT4omini,
        "Deepseek": Deepseek,
        "Gemini 2.5 Flash": Gemini,
        "Gemma": Gemma,
        "QWEN 3-8b": QWEN
    }
