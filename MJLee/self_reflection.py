import openai
import json
from api import api_key
from tqdm import tqdm
import nums_from_string as nfs

textWithoutProblem = f'Please translate it into English, French, and Japanese. During the translation, continuously compare the translation with the original problem to ensure accuracy. Do not attempt to solve the problem during the translation process; only focus on translation.\n' \
f'After completing the translations, treat the four problems as separate problems and solve them in their respective languages. For example, solve the Chinese problem in Chinese, the English problem in English, and so on.\n' \
f'When solving a problem in one language, do not refer to the answers in other languages. For example, do not refer to the English, French, or Japanese versions when solving the Chinese problem. Likewise, when solving the English problem, do not reference other versions.\n' \
f'You must think during the problem-solving process; do not simply output the number without a solving process. At the end of each solution, output only the final answer, and the final answer must be in Arabic numeral format (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).\n' \
f'Once all four language versions are solved, compare the answers and processes to see if they are the same or different. If they differ, identify the incorrect process and answer. If they are the same, ensure the process and answer are correct.\n' \
f'After comparison, confirm one final correct answer. At the very end of the output, only the final answer should be shown, and it must be in Arabic numeral format (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).\n' \
f'Format:\n' \
f'Chinese version\n' \
f'{{Chinese problem}}\n\n' \
f'{{Chinese answer}}\n' \
f'{{Chinese final answer}}\n\n' \
f'English version\n' \
f'{{English problem}}\n\n' \
f'{{English answer}}\n' \
f'{{English final answer}}\n\n' \
f'Japanese version\n' \
f'{{Japanese problem}}\n\n' \
f'{{Japanese answer}}\n' \
f'{{Japanese final answer}}\n\n' \
f'French version\n' \
f'{{French problem}}\n\n' \
f'{{French answer}}\n' \
f'{{French final answer}}\n\n' \
f'{{compare answer}}\n' \
f'{{final answer}}'

openai.api_key = api_key
dir1 = 'mgsm_zh'
dir2 = 'mgsm_en'
nums = 250
prompt = "\nOutput the final answer at the last of your response. If the answer is a number, please output the number only. Arabic numerals only."
prompt_to_output_arabic_number = "(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)"

def self_reflection(data1, data2, result1, result2):
    result = []
    c1c2, w2c1, w1w2, w1c2 = 0, 0, 0, 0
    c1c2_nums, w2c1_nums, w1w2_nums, w1c2_nums = 0, 0, 0, 0
    for i in tqdm(range(nums)):
        text = f'There is a problem:\n\n{result1[i]["output_translate"]}\n\n{textWithoutProblem}'
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
            temperature=0.2
        )
        # print(response["choices"][0]["message"]["content"])
        type = ""
        correct = True if nfs.get_nums(str(data2['answer'][str(i)]))[-1] == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
        if result1[i]['correct'] and result2[i]['correct']:
            c1c2_nums += 1
            c1c2 += 1 if correct else 0
            type = "both correct"
        elif result1[i]['correct'] and not result2[i]['correct']:
            w2c1_nums += 1
            w2c1 += 1 if correct else 0
            type = f'{dir1} correct {dir2} wrong'
        elif not result1[i]['correct'] and not result2[i]['correct']:
            w1w2_nums += 1
            w1w2 += 1 if correct else 0
            type = "both wrong"
        else:
            w1c2_nums += 1
            w1c2 += 1 if correct else 0
            type = f'{dir1} wrong {dir2} correct'

        result.append({"index": i, 
                        "question": text,
                        "output": response["choices"][0]["message"]["content"],
                        "answer": data2['answer'][str(i)],
                        "correct":correct,
                        "type": type
        })
    with open(f'./MJLee/result/mgsm/experiment16.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f'wrong in {dir1}, correct in {dir2}：{w1c2_nums}/{nums}')
    print(f'wrong in {dir2}, correct in {dir1}：{w2c1_nums}/{nums}')
    print(f'wrong in {dir1}, wrong in {dir2}：{w1w2_nums}/{nums}')
    print(f'correct in both：{c1c2_nums}/{nums}')
    print()
    print(f'{dir1}：{c1c2_nums + w2c1_nums}/{nums}')
    print(f'{dir2}：{c1c2_nums + w1c2_nums}/{nums}')
    print("-" * 30)
    print("**After self reflection**")
    print(f'wrong in {dir1}, correct in {dir2}：{w1c2}/{w1c2_nums}')
    print(f'wrong in {dir2}, correct in {dir1}：{w2c1}/{w2c1_nums}')
    print(f'wrong in {dir1}, wrong in {dir2}：{w1w2}/{w1w2_nums}')
    print(f'correct in both：{c1c2}/{c1c2_nums}')
    print()
    print(f'total：{c1c2 + w1c2 + w2c1 + w1w2}/{nums}')


def main():
    with open(f'./data/mgsm/{dir1}_{nums}.json', 'r') as f:
        data1 = json.load(f)
    with open(f'./data/mgsm/{dir2}_{nums}.json', 'r') as f:
        data2 = json.load(f)
    with open(f'./MJLee/result/mgsm/gpt4oMGSMOnly/gpt4o_{dir1}_{nums}.json', 'r') as f:
        result1 = json.load(f)
    with open(f'./MJLee/result/mgsm/MGSM/{dir2}_{nums}.json', 'r') as f:
        result2 = json.load(f)

    self_reflection(data1, data2, result1, result2)
    

if __name__ == '__main__':
    main()