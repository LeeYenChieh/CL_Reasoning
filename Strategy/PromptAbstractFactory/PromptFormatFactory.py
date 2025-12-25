from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory

class PromptFormatFactory(PromptAbstractFactory):
    def __init__(self):
        super().__init__()

    def englishPrompt(self):
        prompt = f'Please strictly follow the format below for output\n' \
            f'Reasoning process\n' \
            f'{{your reasoning process - Note: **Do not restate the original question text or add content not required by the question**}}\n\n' \
            f'Final Answer\n' \
            f'{{"answer":"your answer"}}\n' \
            f'(You shouldn\'t output "your answer" directly. Where "your answer" must and should strictly follow the rules(Usually a English letter or a number) required in the question. The entire final answer block must only be that one line of JSON, with no extra text or explanation before or after.)\n'
        return prompt
    
    def chinesePrompt(self):
        prompt = f'請嚴格遵守以下格式進行輸出\n' \
            f'推理過程\n' \
            f'{{你的推理過程-注意：**不得重述題目原文或在此加入題目未要求的內容**。}}\n\n' \
            f'最終答案\n' \
            f'{{"answer":"your answer"}}\n' \
            f'（其中 你不該直接輸出"your answer"，"your answer" 應該且必須被取代為題目指定的格式(格式通常是一個英文字母或數字)，整個最終答案區塊只能是那一行 JSON，前後不能有其他文字或說明。）\n'
        return prompt
    
    def spanishPrompt(self):
        prompt = f'Por favor, sigue estrictamente el siguiente formato para la salida\n' \
            f'Proceso de razonamiento\n' \
            f'{{tu proceso de razonamiento - Nota: **no debes repetir el texto original de la pregunta ni agregar contenido no solicitado en esta sección**.}}\n\n' \
            f'Respuesta final\n' \
            f'{{"answer":"tu respuesta"}}\n' \
            f'(donde "tu respuesta" debe ser reemplazada por el formato especificado en la pregunta (generalmente una letra o un número), y todo el bloque de la respuesta final debe ser únicamente esa línea JSON, sin texto ni explicaciones adicionales antes o después.)\n'
        return prompt

    def japanesePrompt(self):
        prompt = f'出力には以下の形式を厳守してください\n' \
            f'推論プロセス\n' \
            f'{{あなたの推論プロセス - 注意：**元の質問文を繰り返したり、質問で要求されていない内容を追加したりしないでください**。}}\n\n' \
            f'最終回答\n' \
            f'{{"answer":"your answer"}}\n' \
            f'（ここで "your answer" は直接出力せず、質問で指定された形式（通常は英字または数字）に置き換えてください。最終回答ブロック全体は、そのJSONの1行のみである必要があり、前後に余分なテキストや説明を含めてはいけません。）\n'
        return prompt

    def russianPrompt(self):
        prompt = f'Пожалуйста, строго соблюдайте следующий формат вывода\n' \
            f'Ход рассуждений\n' \
            f'{{ваш ход рассуждений - Примечание: **Не повторяйте исходный текст вопроса и не добавляйте контент, который не требуется в вопросе**}}\n\n' \
            f'Окончательный ответ\n' \
            f'{{"answer":"your answer"}}\n' \
            f'(Где "your answer" не должно выводиться буквально, а должно быть заменено на формат, указанный в вопросе (обычно это английская буква или цифра). Весь блок окончательного ответа должен состоять только из этой одной строки JSON, без какого-либо дополнительного текста или пояснений до или после нее.)\n'
        return prompt