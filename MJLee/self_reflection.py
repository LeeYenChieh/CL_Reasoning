import openai
import json
from api import api_key

openai.api_key = api_key
dir1 = 'mgsm_zh'
dir2 = 'mgsm_en'
nums = 250

def main():
    with open(f'./data/mgsm/{dir1}_{nums}.json', 'r') as f:
        data1 = json.load(f)
    with open(f'./data/mgsm/{dir2}_{nums}.json', 'r') as f:
        data2 = json.load(f)
    with open(f'./MJLee/result/mgsm/{dir1}_{nums}.json', 'r') as f:
        result1 = json.load(f)
    with open(f'./MJLee/result/mgsm/{dir2}_{nums}.json', 'r') as f:
        result2 = json.load(f)
    
    w1c2 = 0
    w2c1 = 0
    w1w2 = 0
    c1c2 = 0
    for i in range(nums):
        if result1[i]['correct'] and result2[i]['correct']:
            c1c2 += 1
        elif result1[i]['correct'] and not result2[i]['correct']:
            w2c1 += 1
        elif not result1[i]['correct'] and not result2[i]['correct']:
            w1w2 += 1
        else:
            w1c2 += 1
    print(f'wrong in {dir1}, correct in {dir2}：{w1c2}/{nums}')
    print(f'wrong in {dir2}, correct in {dir1}：{w2c1}/{nums}')
    print(f'wrong in {dir1}, wrong in {dir2}：{w1w2}/{nums}')
    print(f'correct in both：{c1c2}/{nums}')
    # text = f'問題是 {data1['question'][str(7)]}, 你先前的答案為 {result1[7]['answer']}，請翻譯問題成英文後重頭思考英文的問題並再回答一次並比對兩次的答案並輸出最後的答案'
    # response = openai.ChatCompletion.create(
    #         model="gpt-4o-mini-2024-07-18",
    #         messages=[{"role": "user", "content": text}],
    #     )
    # print(response["choices"][0]["message"]["content"])


if __name__ == '__main__':
    main()