#!/bin/bash

python3 ./main.py --run -m ${1} -d mathqa  -s onlyChinese --nums 6000
python3 ./main.py --run -m ${1} -d commenseqa -s onlyChinese --nums 6000
python3 ./main.py --run -m ${1} -d mmlu -s onlyChinese --nums 6000
python3 ./main.py --run -m ${1} -d truthfulqa -s onlyChinese --nums 6000
