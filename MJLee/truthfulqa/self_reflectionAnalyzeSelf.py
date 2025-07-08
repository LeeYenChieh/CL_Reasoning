import json
import matplotlib.pyplot as plt
import string

def load_result(path):
    with open(path, 'r') as f:
        data = json.load(f)

    return data

def checkCorrect(response, answer):
    letters = list(string.ascii_uppercase)
    correct = False
    try:
        output = response.split()[-1][-1]
        if output not in letters:
            raise TypeError()
        if answer == output:
            correct = True
    except:
        correct = "true/false"
    return correct, output

def main():
    dataset = load_result("./MJLee/truthfulqa/result/experiment8.json")

    ttt, ttf, fft, fff, tft, tff, ftt, ftf = 0, 0, 0, 0, 0, 0, 0, 0
    same = 0
    for i in range(1, 1501):
        responses = dataset[i]["output"]["response"].split("—————————————")
        if len(responses) != 4:
            print(i)
        
        CN_correct, CN_answer = checkCorrect(responses[1], dataset[i]["answer"])
        EN_correct, EN_answer = checkCorrect(responses[2], dataset[i]["answer"])

        if EN_correct and CN_correct and dataset[i]["correct"]:
            ttt += 1
        elif EN_correct and CN_correct and not dataset[i]["correct"]:
            ttf += 1
        elif not EN_correct and not CN_correct and dataset[i]["correct"]:
            fft += 1
        elif not EN_correct and not CN_correct and not dataset[i]["correct"]:
            fff += 1
        elif EN_correct and not CN_correct and dataset[i]["correct"]:
            tft += 1
        elif EN_correct and not CN_correct and not dataset[i]["correct"]:
            tff += 1
        elif not EN_correct and CN_correct and dataset[i]["correct"]:
            ftt += 1
        elif not EN_correct and CN_correct and not dataset[i]["correct"]:
            ftf += 1
        
        if EN_answer != CN_answer:
            same += 1
            print(i)

    print(ttf + ttt)
    print(ftf + ftt)
    print(tff + tft)
    print(fff + fft)
    print(same)

    labels = ["True", "False"]
    sizestt = [ttt / (ttf + ttt), ttf / (ttf + ttt)]
    sizesft = [ftt / (ftf + ftt), ftf / (ftf + ftt)]
    sizestf = [tft / (tff + tft), tff / (tff + tft)]
    sizesff = [fft / (fff + fft), fff / (fff + fft)]

    
    plt.pie(sizesff, labels=labels, autopct='%1.1f%%', startangle=100)
    plt.show()

if __name__ == '__main__':
    main()