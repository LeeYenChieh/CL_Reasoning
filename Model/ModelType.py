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
