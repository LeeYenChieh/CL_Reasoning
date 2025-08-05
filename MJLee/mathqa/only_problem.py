from openai import OpenAI
import json
from api import gpt_api_key
from tqdm import tqdm
import nums_from_string as nfs
import string

client = OpenAI(api_key=gpt_api_key)
nums = 2900
samples = 3
model = "gpt-4.1-mini-2025-04-14"
letters = list(string.ascii_lowercase)

def createPrompt(question, choices):
    prompt = f'There is a Problem: \n{question}.\n' \
    f'And there are 5 choices\n' \
    f'{choices}\n' \
    f'Please choose a choice based on the question\n' \
    f'At the end of the output, provide the answer. The answer must be a single choice and only one English letter (a-e). You cannot output other letters.\n' \
    f'請嚴格遵守以下格式進行輸出，並用英文回答\n' \
    f'推理過程\n' \
    f'{{你的推理過程}}\n\n' \
    f'答案\n' \
    f'{{你的答案(只能是一個英文字母)}}\n'

    return prompt

def sendPromptToModel(prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0
    )

    print(prompt)
    print("=" * 80)
    print(response.choices[0].message.content)

    return {
        "prompt": prompt,
        "response": response.choices[0].message.content
    }


def self_reflection(dataset):
    print(len(dataset))
    result = [{
        "model": model
    }]
    correctCnt = 0
    notSureCnt = 0

    pbar = tqdm(total=samples * nums)
    for i in range(nums):
        prompt = createPrompt(dataset[i]["Problem"], dataset[i]["options"])

        for j in range(samples):
            response = sendPromptToModel(prompt)

            # check answer
            correct = False
            try:
                answer = dataset[i]["correct"]
                output = response["response"].split('\n')[-1][-1]
                if output not in letters:
                    raise TypeError()
                if answer == output:
                    correct = True
                    correctCnt += 1
            except:
                correct = "true/false"
                notSureCnt += 1
            print(correct)
            print(f'correct：{correctCnt}/{i * samples + j + 1}')
            print(f'notSure：{notSureCnt}/{i * samples + j + 1}')

            result.append({"index": i * samples + j, 
                            "question": prompt,
                            "output": response,
                            "answer": dataset[i]["correct"],
                            "correct":correct,
            })
            pbar.update(1)
    with open(f'./MJLee/mathqa/result/experiment5.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


    pbar.close()

    print(f'correct：{correctCnt}/{nums * samples}')
    print(f'notSure：{notSureCnt}/{nums * samples}')

def load_dataset(json_path):
    with open(f'./MJLee/mathqa/{json_path}', 'r') as f:
        data = json.load(f)
    return data[0:nums]

def main():
    dataset = load_dataset("test.json")
    self_reflection(dataset)


if __name__ == '__main__':
    main()