import openai
import json
from api import api_key
from tqdm import tqdm
import nums_from_string as nfs

textWithoutProblem = f'Please translate it into English and Chinese. During the translation, continuously compare the translation with the original problem to ensure accuracy. Do not attempt to solve the problem during the translation process; only focus on translation.\n' \
f'After completing the translations, treat the two problems as separate problems and solve them in their respective languages. For example, solve the Chinese problem in Chinese, the English problem in English, and so on.\n' \
f'You are now going to simulate two AI assistants, each operating in a different language: a Chinese assistant and an English assistant must independently think and solve the problem based solely on the version of the question written in their respective language. Please simulate the behavior of the two assistants one by one, ensuring complete independence between them. \n' \
f'When solving a problem in one language, please ignore all your previous answers to this question. Think about it again from scratch and answer it as if you\'re seeing it for the first time. Do not refer to the answers in other languages. For example, do not refer to the English versions when solving the Chinese problem. Likewise, when solving the English problem, do not reference other versions.\n' \
f'You must think during the problem-solving process; do not simply output the number without a solving process. At the end of each solution, output only the final answer, and the final answer must be "choice 1" or "choice 2".\n' \
f'Once all two language versions are solved, compare the answers and processes to see if they are the same or different. If they differ, identify the incorrect process and output the correct answer. If they are the same, ensure the process and answer are correct.\n' \
f'After comparison, confirm one final correct answer. At the very end of the output, only the final answer should be shown, and it must be "choice 1" or "choice 2".\n'

outputFormat = f'You must strictly follow the output format below.\n' \
f'Format:\n' \
f'English Problem\n' \
f'{{English Problem}}\n\n' \
f'Chinese Problem\n' \
f'{{Chinese Problem}}\n\n' \
f'English Answer\n' \
f'{{English Answer}}\n' \
f'{{English Final Answer}}\n\n' \
f'Chinese Answer\n' \
f'{{Chinese Answer}}\n' \
f'{{Chinese Final Answer}}\n\n' \
f'Compare Answer\n' \
f'{{Compare Answer}}\n\n' \
f'Final Answer\n' \
f'{{Final Answer}}'

openai.api_key = api_key
nums = 500

def self_reflection(zh_data, en_data):
    result = []
    cnt = 0
    for i in tqdm(range(nums)):
        problem = f'There is a premise: {zh_data[i]["premise"]}.\n' \
        f'We want to know what the {zh_data[i]["question"]} may be. \n' \
        f'There are two choice, and you should choose the most possible choice. \n' \
        f'choice 1: {zh_data[i]["choice1"]}\n' \
        f'choice 2: {zh_data[i]["choice2"]}\n'
        text = f'There is a problem:\n\n{problem}\n\n{textWithoutProblem + outputFormat}'
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
            temperature=0.2
        )
        print(response["choices"][0]["message"]["content"])
        correct = True if zh_data[i]["label"] + 1 == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
        if correct:
            cnt += 1
        result.append({"index": i, 
                        "question": text,
                        "output": response["choices"][0]["message"]["content"],
                        "answer": f'choice {zh_data[i]["label"] + 1}',
                        "correct":correct,
        })
    with open(f'./MJLee/xcopa/result/experiment1.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f'total：{cnt}/{nums}')

def load_jsonl(jsonl_file):
    data = []
    with open(jsonl_file, "r") as file:
        for line in file:
            json_obj = json.loads(line)
            data.append(json_obj)
    return data

def main():
    zh_data = load_jsonl(f'./data/xcopa/data/zh/test_zh.jsonl')
    en_data = load_jsonl(f'./data/xcopa/data-gmt/zh/test_zh.jsonl')

    self_reflection(zh_data, en_data)
    

if __name__ == '__main__':
    main()