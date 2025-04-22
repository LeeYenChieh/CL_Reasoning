import json
import nums_from_string as nfs
import re

language_headers = ['Chinese version', 'English version', 'Japanese version', 'French version', 'compare answer', 'final answer']

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

def find_inconsistent_values(data: dict, index):
    if not data:
        return []

    # 取得所有的值組成的 set，若只有一個值，代表都相等
    unique_values = set(data.values())

    if len(unique_values) == 1:
        return

    # 否則，找出與多數不同的 key
    print(f'❌ Values are not all equal. {index}')
    print(data)


def main():
    with open(f'./MJLee/result/mgsm/experiment16.json', 'r') as f:
        outputs = json.load(f)
    cnt = {
        'Chinese version': 0,
        'English version': 0,
        'Japanese version': 0,
        'French version': 0,
        'compare answer': 0,
        'final answer': 0
    }
    i = 0
    for output in outputs:
        answers = find_answer(output["output"])
        find_inconsistent_values(answers, output["index"])
        questionAnswer = nfs.get_nums(output["answer"])[0]
        for lang, answer in answers.items():
            if questionAnswer == answer:
                cnt[lang] += 1
    for lang, answer in cnt.items():
        print(f"{lang}: {answer}")


if __name__ == '__main__':
    main()