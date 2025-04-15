import openai
import json
from api import api_key
from tqdm import tqdm
import nums_from_string as nfs


openai.api_key = api_key
dir1 = 'mgsm_zh'
dir2 = 'mgsm_en'
nums = 250
prompt = "\n請在輸出的最後輸出答案，最後的輸出只能有數字，數字必須為阿拉伯數字的格式"

def self_reflection(data1, data2, result1, result2):
    result = []
    c1c2, w2c1, w1w2, w1c2 = 0, 0, 0, 0
    c1c2_nums, w2c1_nums, w1w2_nums, w1c2_nums = 0, 0, 0, 0
    for i in tqdm(range(nums)):
        text = f'There is a problem:\n\n{result1["output_translate"] + prompt}\n\nWe have two answer.\n\nTne answer is "{result1[i]["output"]}"\n\nThe other answer is "{result2[i]["output"]}"\n\nPlease compare the two answers. If there are any errors in their calculations or steps, please correct them. If there are no errors, check whether both answers correctly address the question and whether their reasoning is logically sound. Finally, provide the solution and answer you believe to be correct.' + prompt
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
            temperature=0.2
        )
        correct = True if nfs.get_nums(str(data2['answer'][str(i)]))[-1] == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
        if result1[i]['correct'] and result2[i]['correct']:
            c1c2_nums += 1
            c1c2 += 1 if correct else 0
        elif result1[i]['correct'] and not result2[i]['correct']:
            w2c1_nums += 1
            w2c1 += 1 if correct else 0
        elif not result1[i]['correct'] and not result2[i]['correct']:
            w1w2_nums += 1
            w1w2 += 1 if correct else 0
        else:
            w1c2_nums += 1
            w1c2 += 1 if correct else 0

        result.append({"index": i, 
                        "question": text,
                        "output": response["choices"][0]["message"]["content"],
                        "answer": data2['answer'][str(i)],
                        "correct":correct
        })
    with open(f'./MJLee/result/mgsm/experiment14.json', 'w', encoding='utf-8') as f:
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