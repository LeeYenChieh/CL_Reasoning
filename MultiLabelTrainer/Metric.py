from sklearn.metrics import accuracy_score, fbeta_score, accuracy_score, precision_score
import torch
import numpy as np

def multi_label_metrics(predictions, labels, threshold=0.5):
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(torch.Tensor(predictions))
    
    # 預測轉換
    y_pred = np.zeros(probs.shape)
    y_pred[probs >= threshold] = 1
    
    # 使用 fbeta_score，並設定 beta=0.5
    # beta < 1: 重視 Precision (鼓勵猜 0)
    # beta > 1: 重視 Recall (鼓勵猜 1)
    f05_micro = fbeta_score(labels, y_pred, beta=0.5, average='micro')
    
    # 也可以直接監控 Precision
    precision = precision_score(labels, y_pred, average='micro')
    
    return {
        "f0.5_micro": f05_micro,  # 主要看這個
        "precision": precision,
        "accuracy": accuracy_score(labels, y_pred)
    }

def compute_metrics(p):
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    result = multi_label_metrics(predictions=preds, labels=p.label_ids)
    return result