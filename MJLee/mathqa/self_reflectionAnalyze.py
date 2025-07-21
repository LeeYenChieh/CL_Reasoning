import json
import matplotlib.pyplot as plt

nums = 500
samples = 1

def load_result(path1, path2, path3, path4):
    with open(path1, 'r') as f:
        data1 = json.load(f)
    with open(path2, 'r') as f:
        data2 = json.load(f)
    with open(path3, 'r') as f:
        data3 = json.load(f)
    with open(path4, 'r') as f:
        data4 = json.load(f)

    return {
        "data1": data1,
        "data2": data2,
        # "data3": data3,
        "data4": data4,
    }

def main():
    dataset = load_result("./MJLee/mathqa/result/experiment1.json", "./MJLee/mathqa/result/experiment2.json", "./MJLee/mathqa/result/experiment3.json", "./MJLee/mathqa/result/experiment4.json")
    ttt, ttf, fft, fff, tft, tff, ftt, ftf = 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(1, nums * samples + 1):
        if dataset["data1"][i]["correct"] and dataset["data2"][i]["correct"] and dataset["data4"][i]["correct"]:
            ttt += 1
        elif dataset["data1"][i]["correct"] and dataset["data2"][i]["correct"] and not dataset["data4"][i]["correct"]:
            ttf += 1
        elif not dataset["data1"][i]["correct"] and not dataset["data2"][i]["correct"] and dataset["data4"][i]["correct"]:
            fft += 1
            print(i)
        elif not dataset["data1"][i]["correct"] and not dataset["data2"][i]["correct"] and not dataset["data4"][i]["correct"]:
            fff += 1
        elif dataset["data1"][i]["correct"] and not dataset["data2"][i]["correct"] and dataset["data4"][i]["correct"]:
            tft += 1
        elif dataset["data1"][i]["correct"] and not dataset["data2"][i]["correct"] and not dataset["data4"][i]["correct"]:
            tff += 1
        elif not dataset["data1"][i]["correct"] and dataset["data2"][i]["correct"] and dataset["data4"][i]["correct"]:
            ftt += 1
        elif not dataset["data1"][i]["correct"] and dataset["data2"][i]["correct"] and not dataset["data4"][i]["correct"]:
            ftf += 1

    print(ttf + ttt)
    print(ftf + ftt)
    print(tff + tft)
    print(fff + fft)

    labels = ["True", "False"]
    sizestt = [ttt / (ttf + ttt), ttf / (ttf + ttt)]
    sizesft = [ftt / (ftf + ftt), ftf / (ftf + ftt)]
    sizestf = [tft / (tff + tft), tff / (tff + tft)]
    sizesff = [fft / (fff + fft), fff / (fff + fft)]

    plt.pie(sizesff, labels=labels, autopct='%1.1f%%', startangle=100)
    plt.show()

if __name__ == '__main__':
    main()