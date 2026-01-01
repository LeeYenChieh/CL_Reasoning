import torch
from torch import nn
from transformers import Trainer

class ConservativeTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None): # 相容性更新
        labels = inputs.get("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")
        
        # --- 🔥 關鍵修改：懲罰「猜 1」的行為 ---
        # 設定 pos_weight < 1 (例如 0.3)
        # 意義：正樣本(1) 的權重變小 -> 變相放大了 負樣本(0) 的權重
        # 這會強迫模型只有在非常有把握時才敢猜 1
        
        # 您可以先設 0.3 試試看 (數值越小，模型越保守，越愛猜 0)
        weights = torch.full((logits.shape[1],), 0.6).to(logits.device) 
        
        loss_fct = nn.BCEWithLogitsLoss(pos_weight=weights)
        loss = loss_fct(logits, labels)
        
        return (loss, outputs) if return_outputs else loss