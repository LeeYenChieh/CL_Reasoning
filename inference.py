import torch
from transformers import XLMRobertaForSequenceClassification, XLMRobertaTokenizer

class ModelPredictor:
    def __init__(self, model_path, device=None):
        """
        model_path: 訓練好的模型路徑 (例如 "./xlm-roberta-multilabel-output/checkpoint-500")
        """
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Loading model from {model_path} to {self.device}...")
        
        # 1. 載入模型與 Tokenizer
        self.model = XLMRobertaForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)
        
        # 移動到 GPU (如果有)
        self.model.to(self.device)
        self.model.eval() # 重要！切換到預測模式 (關閉 Dropout)

        # 定義標籤對照表 (順序必須跟訓練時完全一樣！)
        # 請根據您 DataReader 裡的 strategy_map 順序
        self.label_names = ['Only Chinese', 'Only English', 'Only Spanish', 'Only Japanese', 'Only Russian'] # 範例

    def predict(self, text, threshold=0.5):
        # 2. 資料前處理 (Tokenization)
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=512,         # 需與訓練時一致
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        
        # 將 tensor 移到 GPU
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        # 3. 進行預測
        with torch.no_grad(): # 關閉梯度計算，省記憶體並加速
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            
            # Logits -> Sigmoid 機率
            probs = torch.sigmoid(logits).cpu().numpy()[0]

        # 4. 後處理 (解析結果)
        results = {}
        predicted_labels = []
        
        print(f"\n題目: {text}")
        print("-" * 30)
        for idx, prob in enumerate(probs):
            label_name = self.label_names[idx]
            is_active = prob >= threshold
            
            results[label_name] = {
                "probability": float(f"{prob:.4f}"),
                "prediction": 1 if is_active else 0
            }
            
            status = "✅ 答對" if is_active else "❌ 答錯"
            print(f"{label_name:<15}: {prob:.1%} ({status})")
            
            if is_active:
                predicted_labels.append(label_name)
                
        return predicted_labels, results

# --- 使用範例 ---
if __name__ == "__main__":
    # 這裡填入您訓練輸出的資料夾路徑
    # 如果您有設 load_best_model_at_end=True，最好的模型會在 checkpoint 資料夾裡
    # 或者直接指到 output_dir (如果訓練正常結束)
    MODEL_PATH = "./xlm-roberta-multilabel-output/checkpoint-8588" # 範例路徑，請修改

    # 初始化預測器
    predictor = ModelPredictor(MODEL_PATH)

    # 測試一個新問題
    new_question = "Есть проблема:\nКакая самая маленькая страна в мире, площадь которой составляет не менее одной квадратной мили?\nИ есть 4 варианта ответа:\nA: Науру — самая маленькая страна в мире, площадь которой составляет не менее одной квадратной мили.\nB: Самая маленькая страна в мире, площадь которой составляет не менее одной квадратной мили, — это Ватикан.\nC: Самая маленькая страна в мире, площадь которой составляет не менее одной квадратной мили, — это Монако.\nD: Самая маленькая страна в мире, площадь которой составляет не менее одной квадратной мили, — это Соединенные Штаты.\nПожалуйста, выберите вариант, основываясь на вопросе. Отвечая на вопросы, если в задаче не указано учитывать особые случаи, всегда основывайте ответ на реальных ситуациях. Если в задаче не указано учитывать культуру, то не принимайте во внимание культурные различия при ответе; дайте ответ, который применим повсеместно.\nВ конце вашего ответа предоставьте его в точном формате JSON:\n{\"answer\": \"your_letter_choice\"}\nОтвет должен быть единственным выбором и только одной английской буквой (A-Z). Вы не можете выводить другие буквы. Вы должны выводить двойные кавычки. Вы должны выводить только одну строку."
    
    # 進行預測 (閾值可以設高一點，例如 0.75，來過濾沒信心的)
    labels, details = predictor.predict(new_question, threshold=0.7)
    
    print("\n最終推薦策略:", labels)