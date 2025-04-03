import openai
import json
from api import api_key

openai.api_key = api_key
dir1 = 'mgsm_zh'
dir2 = 'mgsm_en'
nums = 50

def main():
    with open(f'./data/mgsm/{dir1}_{nums}.json', 'r') as f:
        data = json.load(f)
    with open(f'./result/mgsm/{dir1}_{nums}.json', 'r') as f:
        result1 = json.load(f)
    with open(f'./result/mgsm/{dir2}_{nums}.json', 'r') as f:
        result2 = json.load(f)
    text = f'問題是 {data['question'][str(7)]}, 你先前的答案為 {result1[7]['answer']}，請翻譯問題成英文後重頭思考英文的問題並再回答一次並比對兩次的答案並輸出最後的答案'
    response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
        )
    print(response["choices"][0]["message"]["content"])


if __name__ == '__main__':
    main()