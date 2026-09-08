from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory


class PromptRewriteFactory(PromptAbstractFactory):
    """
    Builds the prompt used for Experiment 1: paraphrasing a question stem.

    The model must reword the stem only. Numbers, names, units and — crucially — the answer
    options must be reproduced verbatim, and the original instructions / answer-format
    requirements must be preserved. The guardrails mirror PromptTranslateFactory: the model
    must NOT solve the question and must NOT emit any JSON answer.
    """
    def __init__(self):
        super().__init__()

    def englishPrompt(self, question: str):
        prompt = (
            'Rewrite the question stem using different wording while preserving the exact '
            'meaning. Do NOT change any numbers, names, units, or answer options. Output the '
            'answer options verbatim. Keep every instruction and answer-format requirement. '
            'Do NOT solve the question, do NOT output any JSON answer, and do NOT add comments. '
            'Output only the rewritten question.\n```\n' + question + '\n```\n'
        )
        return prompt

    def chinesePrompt(self, question: str):
        prompt = (
            '用不同的措辭改寫以下題目的題幹，同時完整保留原本的意思。不要更動任何數字、名稱、單位或選項。'
            '選項必須原封不動地輸出。保留所有說明與作答格式要求。不要解題，不要輸出任何 JSON 答案，也不要加入任何註解。'
            '只輸出改寫後的題目。\n```\n' + question + '\n```\n'
        )
        return prompt

    def spanishPrompt(self, question: str):
        prompt = (
            'Reescribe el enunciado de la pregunta con una redacción diferente, preservando '
            'exactamente el mismo significado. NO cambies ningún número, nombre, unidad ni las '
            'opciones de respuesta. Reproduce las opciones de respuesta de forma literal. '
            'Conserva todas las instrucciones y los requisitos de formato de la respuesta. NO '
            'resuelvas la pregunta, NO generes ninguna respuesta en JSON y no añadas comentarios. '
            'Devuelve únicamente la pregunta reescrita.\n```\n' + question + '\n```\n'
        )
        return prompt

    def japanesePrompt(self, question: str):
        prompt = (
            '以下の問題文（設問部分）を、意味を完全に保ったまま別の言い回しで書き換えてください。'
            '数字・名前・単位・選択肢は一切変更しないでください。選択肢はそのまま逐語的に出力してください。'
            'すべての指示と解答フォーマットの要件は保持してください。問題を解かないでください。'
            'JSON形式の解答は一切出力せず、コメントも追加しないでください。書き換えた問題のみを出力してください。'
            '\n```\n' + question + '\n```\n'
        )
        return prompt

    def russianPrompt(self, question: str):
        prompt = (
            'Перефразируйте формулировку вопроса другими словами, полностью сохранив исходный '
            'смысл. НЕ изменяйте числа, имена, единицы измерения и варианты ответа. Варианты '
            'ответа выведите дословно. Сохраните все инструкции и требования к формату ответа. '
            'НЕ решайте задачу, НЕ выводите никакого ответа в формате JSON и не добавляйте '
            'комментариев. Выведите только перефразированный вопрос.\n```\n' + question + '\n```\n'
        )
        return prompt
