import json
import nums_from_string as nfs
import re

# language_headers = ['Chinese version', 'English version', 'compare answer', 'final answer']
language_headers = ['Chinese Answer', 'English Answer', 'Compare Answer', 'Final Answer']

def find_answer(text):
    # 用正則式將每個語言段分割出來
    segments = {}
    for i in range(len(language_headers)):
        start_header = language_headers[i]
        end_header = language_headers[i + 1] if i + 1 < len(language_headers) else None

        # 找出起始位置
        start_index = text.find(start_header)
        if start_index == -1:
            continue
        start_index += len(start_header)

        # 找出結束位置（如果有下一段）
        if end_header:
            end_index = text.find(end_header)
            content = text[start_index:end_index].strip()
        else:
            content = text[start_index:].strip()

        segments[start_header] = content

    # 用 nums_from_string 抽出最終答案
    answers = {}
    for lang, content in segments.items():
        nums = nfs.get_nums(content)
        if nums:
            answers[lang] = int(nums[-1])

    # 輸出結果
    return answers

def main():
    with open(f'./MJLee/result/mgsm/experiment20.json', 'r') as f:
        outputs = json.load(f)
    cnt = {
        'Chinese Answer': 0,
        'English Answer': 0,
        'Compare Answer': 0,
        'Final Answer': 0
    }
    i = 0
    for output in outputs:
        answers = find_answer(output["output"])
        questionAnswer = nfs.get_nums(output["answer"])[0]
        errorString = ""
        for lang, answer in answers.items():
            if questionAnswer == answer:
                cnt[lang] += 1
            else:
                if errorString == "":
                    errorString = "❌ error"
                errorString += f' {lang}'
        if errorString != "":
            errorString += f' {output['index']}'
            print(errorString)
    for lang, answer in cnt.items():
        print(f"{lang}: {answer}")


if __name__ == '__main__':
    main()