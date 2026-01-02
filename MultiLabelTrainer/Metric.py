from sklearn.metrics import accuracy_score, fbeta_score, accuracy_score, precision_score
import torch
import numpy as np

import numpy as np
from sklearn.metrics import fbeta_score, accuracy_score, precision_score
import torch

def multi_label_metrics(predictions, labels, threshold=0.5):
    # 1. 轉成 Sigmoid 機率
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(torch.Tensor(predictions))
    
    # 2. 轉成 0/1 預測
    y_pred = np.zeros(probs.shape)
    y_pred[probs >= threshold] = 1
    
    # --- 🔥 關鍵修正開始 ---
    # Scikit-learn 不支援 -100，我們必須手動過濾掉
    
    # 建立遮罩：找出哪些標籤不是 -100 (有效標籤)
    mask = (labels != -100)
    
    # 利用遮罩取出有效資料 (這會自動把二維陣列攤平成一維)
    # 例如: labels=[[1, -100], [0, 1]] -> filtered_labels=[1, 0, 1]
    y_true_filtered = labels[mask]
    y_pred_filtered = y_pred[mask]
    
    # --- 🔥 關鍵修正結束 ---

    # 3. 計算指標 (使用過濾後的資料)
    # 因為已經攤平成一維了，這裡算出來的其實就是 Micro 的概念 (Global count)
    
    if len(y_true_filtered) == 0:
        return {
            "f0.5_micro": 0.0,
            "precision": 0.0,
            "accuracy": 0.0
        }

    f05_micro = fbeta_score(y_true_filtered, y_pred_filtered, beta=0.5, average='micro')
    precision = precision_score(y_true_filtered, y_pred_filtered, average='micro', zero_division=0)
    
    # 注意：這裡的 Accuracy 變成了「格子級別」的準確率 (Cell-wise Accuracy)
    # 也就是：(所有猜對的格子數) / (所有有效格子數)
    accuracy = accuracy_score(y_true_filtered, y_pred_filtered)
    
    return {
        "f0.5_micro": f05_micro,
        "precision": precision,
        "accuracy": accuracy
    }

def compute_metrics(p):
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    result = multi_label_metrics(predictions=preds, labels=p.label_ids)
    return result