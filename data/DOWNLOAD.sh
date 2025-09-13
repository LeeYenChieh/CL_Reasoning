#!/usr/bin/env bash

# Download and extract MMLU dataset
if [ ! -d "mmlu" ]; then
    if [ ! -f "mmlu_data.tar" ]; then
        echo "Downloading MMLU dataset..."
        wget -O mmlu_data.tar "https://people.eecs.berkeley.edu/~hendrycks/data.tar"
        if [ $? -ne 0 ]; then
            echo "Failed to download MMLU dataset. Please check your internet connection."
            exit 1
        fi
    fi
    
    echo "Extracting MMLU dataset from mmlu_data.tar..."
    tar -xf mmlu_data.tar
    mv data mmlu
    echo "MMLU dataset extracted to mmlu/ directory"
fi

# Download TruthfulQA dataset  
if [ ! -d "truthfulqa" ]; then
    git clone https://github.com/sylinrl/TruthfulQA.git truthfulqa
fi

# Download XCOPA dataset
if [ ! -d "xcopa" ]; then
    git clone https://github.com/cambridgeltl/xcopa.git xcopa
fi

# Download MGSM dataset (if zip file exists)
if [ -f "mgsm.zip" ]; then
    unzip mgsm.zip
fi

echo "Dataset download completed!"
echo "Available datasets:"
echo "- MathQA: mathqa.json"
echo "- MMLU: mmlu/test/ (extracted from mmlu_data.tar)"
echo "- TruthfulQA: truthfulqa/"
echo "- XCOPA: xcopa/"