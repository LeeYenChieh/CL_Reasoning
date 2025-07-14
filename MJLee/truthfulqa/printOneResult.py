import json

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
        "data3": data3,
        "data4": data4,
    }

def main():
    dataset = load_result("./MJLee/truthfulqa/result/experiment13.json", "./MJLee/truthfulqa/result/experiment14.json", "./MJLee/truthfulqa/result/experiment15.json", "./MJLee/truthfulqa/result/experiment16.json")
    index = int(input())
    print(index)
    print("=" * 50)
    print("Experiment1")
    print(dataset["data1"][index]["output"]["prompt"])
    print(dataset["data1"][index]["output"]["response"])
    print("=" * 50)
    print("Experiment2")
    print(dataset["data2"][index]["output"]["prompt"])
    print(dataset["data2"][index]["output"]["translate"])
    print(dataset["data2"][index]["output"]["response"])
    print("=" * 50)
    print("Experiment3")
    print(dataset["data3"][index]["output"]["prompt"])
    print(dataset["data3"][index]["output"]["response"])
    print("=" * 50)
    print("Experiment4")
    print(dataset["data4"][index]["output"]["prompt"])
    print(dataset["data4"][index]["output"]["response"])

if __name__ == '__main__':
    main()