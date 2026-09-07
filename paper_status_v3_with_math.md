# 論文現況整理 v3（含完整數學說明）

> 更新日期：2026-09-05
> **本文取代 v1、v2。** 每一處數學分析都附有方法解釋與變數定義。
> 標記說明：📐 = 數學方法解釋　🔴 = 關鍵未解　✅ = 已完成　⚠️ = 需重跑

---

## 目錄

0. [符號總表](#0-符號總表)
1. [最初的困境](#1-最初的困境)
2. [實驗結果盤點與文獻對照](#2-實驗結果盤點與文獻對照)
3. [建議的新方向](#3-建議的新方向)
4. [新論文的完整邏輯流程](#4-新論文的完整邏輯流程)
5. [待辦清單與各階段上稿機率](#5-待辦清單與各階段上稿機率)
6. [完整參考文獻稽核表](#6-完整參考文獻稽核表)
7. [數學方法附錄](#7-數學方法附錄)

---

## 0. 符號總表

先把所有會用到的變數列出來。**pp = percentage point（百分點）**，例如 82.25% 與 80.15% 相差 2.10pp。

### 基本量

| 符號 | 全名 | 中文意思 | 怎麼算 | 實測範圍 |
|---|---|---|---|---|
| `a_A` | monolingual accuracy of language A | 只用語言 A 單獨作答的準確率 | 直接跑 baseline | 0.65 – 0.93 |
| `pair_acc` | pair accuracy | 語言 A、B 配對辯論後的準確率 | 跑 IMSR pipeline | 0.70 – 0.92 |
| `max` | — | 兩個語言中**較強**那個的單語準確率 | `max(a_A, a_B)` | — |
| `min` | — | 兩個語言中**較弱**那個的單語準確率 | `min(a_A, a_B)` | — |
| `gap` | capability gap | 兩語言的**能力落差** | `max − min` | 0.1 – 11.9pp |
| `excess` | — | 配對比「單獨用強語言」好多少 | `pair_acc − max` | −2.0 – +4.4pp |

### 辯論流程的量

| 符號 | 中文意思 | 怎麼算 | 實測範圍 |
|---|---|---|---|
| `d` | **分歧率**：兩個 agent 初始答案不同的比例 | 不一致題數 / 總題數 | 0.039 – 0.238 |
| `a_agree` | **一致時的準確率** | 在一致的題目中答對的比例 | 0.695 – 0.933 |
| `acc_debate` | **辯論後的準確率** | 在不一致的題目中，經辯論最終答對的比例 | 0.430 – 0.642 |
| `c` | **可回收率**：不一致時至少有一方原本就答對的比例 | 不一致題目中「恰好一方答對」的比例 | 0.634 – 0.838 |
| `recovery` | **裁決品質**：裁決者吃到了多少可用空間 | `(acc_debate − c/2) / (c/2)` | 0.159 – 0.573 |

### 迴歸係數

| 符號 | 中文意思 | 來自哪個式子 | 實測 |
|---|---|---|---|
| `a_excess` | **綜效紅利**：兩語言等強時，配對比單用強語言好多少 | `excess = a_excess + g_excess·gap` 的截距 | +2.44pp |
| `g_excess` | **落差代價**：gap 每增加 1pp，excess 掉多少 | 上式的斜率 | −0.412 |
| `gap*` | **損益兩平點**：gap 超過這個值，配對就開始虧損 | `a_excess / \|g_excess\|` | ≈ 5.9pp |
| `b_max` | 強語言的權重 | `pair_acc = b_max·max + b_min·min` | 0.438 |
| `b_min` | 弱語言的權重 | 同上 | 0.231 |

### 統計量

| 符號 | 中文意思 |
|---|---|
| `SE` | 標準誤（standard error）：估計值的浮動幅度 |
| `t` | t 值：估計值是標準誤的幾倍 |
| `p` | p 值：如果真實效果為零，你觀察到這麼極端的結果的機率 |
| `R²` | 決定係數：迴歸線解釋了資料變異的百分之幾 |
| `SD` | 標準差（standard deviation）：一組數字的散布程度 |

---

## 1. 最初的困境

### 1.1 原本的主張

**Iterative Multilingual Self-Reflection (IMSR)**：同一 LLM 以兩種語言扮演兩個 agent，答案不一致時進入最多 3 輪跨語言辯論，無共識則由 Judgment Agent 裁決。另用 fine-tuned XLM-RoBERTa 從 10 個語言對中動態預測最可能成功修正的一對。

### 1.2 ARR 評分

| Reviewer | Soundness | Excitement | Overall | Confidence |
|---|---|---|---|---|
| R1 | 2.5 | 2.5 | 2.5（Borderline Findings） | 4 |
| R2 | 2.0 | 2.5 | 2.0（Resubmit next cycle） | 4 |
| R3 | 2.0 | 1.5 | 1.5（Resubmit **after** next cycle） | **5** |

### 1.3 核心批評與 v3 狀態

| 編號 | 批評 | 提出者 | v3 狀態 |
|---|---|---|---|
| **W1** | 跨語言多樣性的因果角色未建立，缺同語言雙 agent 對照 | R1 | 🔴 **仍是最關鍵的未解問題**（§2.7） |
| W2 | 五種語言的選擇缺乏理據 | R1 | 🟢 已解：語言選擇規則由損益兩平公式給出 |
| W3 | Router 泛化範圍未討論 | R1, R2 | 🟢 已解：router 不需要存在 |
| N1 | Novelty 不足，只是既有技術的組合 | R2 | 🟢 已解：損益兩平分析是新的 |
| N2 | 未討論 AutoCAP、mGRPO | R2 | 🟡 待補引用與 baseline |
| C1 | 只有 17 篇引用；§2.4 完全無 citation | R3 | 🟡 待補 |
| C2 | 顯著性檢定不透明 | R3 | 🟡 待補 |
| C3 | Mixed-code 辯論的穩定性存疑 | R3 | 🟡 待做 ablation |
| C4 | Best Fixed Pair 為何在模型間飄移？ | R3 | 🟢 **已解**（§2.5） |
| C5 | SR 與 IMSR 的輪數是否對齊？ | R3 | 🟡 待對齊 |
| R | Reproducibility / Datasets / Software 全低分 | 全員 | 🟡 待釋出 |

### 1.4 內部困境

XLM-RoBERTa router 訓不起來。**現已查明：不是 bug，是任務本身不存在 query-level 訊號。**

---

## 2. 實驗結果盤點與文獻對照

### 2.1 Router 塌縮成常數函數 ✅

| 模型 | 最大宗語言對佔比 | 有效對數 (2^H) | top1−top2 邊際中位數 |
|---|---|---|---|
| gpt4o-mini | 100.00% | **1.00** | 0.0329 |
| deepseek | 98.76% | **1.07** | 0.0253 |
| gemini | 76.66% | 1.98 | 0.0059 |
| qwen | 39.44% | 3.47 | 0.0049 |

> ### 📐 「有效對數 2^H」是什麼
>
> 這是用**熵（entropy）**來衡量「router 實際上用了幾種選項」。
>
> 假設 router 選 10 個語言對的比例分別是 `p₁, p₂, ..., p₁₀`（加起來等於 1）。熵的定義是：
>
> ```
> H = − Σ pᵢ · log₂(pᵢ)
> ```
>
> 熵衡量「不確定性」。兩個極端：
>
> - **全部選同一對**（p₁=1，其餘=0）→ `H = −1·log₂(1) = 0` → `2^H = 2⁰ = 1`
> - **10 對均勻分配**（每個 pᵢ=0.1）→ `H = −10 × 0.1 × log₂(0.1) = 3.32` → `2^H = 10`
>
> 所以 `2^H` 可以直接讀成「**等效於在幾個選項之間做選擇**」。
>
> 你的 gpt4o-mini 是 `2^H = 1.00`，意思是它等效於**完全沒有在選**——永遠輸出同一個答案。
>
> **實例計算**（deepseek）：english_vs_japanese 佔 98.76%、english_vs_russian 佔 1.24%
> ```
> H = −(0.9876 × log₂0.9876 + 0.0124 × log₂0.0124)
>   = −(0.9876 × (−0.0180) + 0.0124 × (−6.333))
>   = 0.0178 + 0.0785 = 0.0963
> 2^H = 2^0.0963 = 1.069  ✓ 對應表中的 1.07
> ```

> ### 📐 「top1−top2 邊際」是什麼
>
> Router 對 10 個語言對各輸出一個機率。把它們由大到小排序，最高的減去第二高的，就是「邊際」。
>
> 邊際大 → router 對自己的選擇有信心，換一個 query 也不會改變選擇。
> 邊際小 → 最高與第二高幾乎並列，只要有一點雜訊，argmax 就會翻掉。
>
> 你的邊際是 0.005–0.033，而模型輸出的機率本身在 0.30–0.44 之間。**邊際只有機率量級的 1–8%**，代表 router 對 10 個選項給出的分數幾乎相同——它輸出的實質上只有一個常數向量加上微小雜訊。

**補充證據**：
- Router 在 3/4 模型選錯最佳固定對（gemini 差 −5.3pp）
- 輸出隨輸入語言變動（gemini 33.6%、qwen 50.4%），**但標籤是語言不變的**（同一題的 5 個語言版本共用同一個 y）→ 這些變動 100% 是雜訊
- 預測機率全落在 0.30–0.44，實際 base rate 約 50% → 可能訓練不足，需重跑確認

**佐證文獻**：

> **The Routing Plateau**（arXiv 2606.07587）
> **要引用的論點**：21 種 routing 方法 × 5 benchmark 全部塌縮到遠低於 oracle 的窄帶；瓶頸在 correctness prediction；router 學到的是粗粒度的全域模型能力趨勢，而非 hard query 所需的 instance-specific 訊號；擴大資料、換更強 encoder、end-to-end fine-tune 最多再拉 2.13pp。
> **用途**：把我們的 router 失敗從「實作問題」升級為「複現一個已知的結構性限制，並首次在多語言情境下量化它」。

---

### 2.2 Table 2 重新分析 ✅

| 比較 | 平均差 | 勝負 |
|---|---|---|
| IMSR − Random Pair | +1.57pp | — |
| IMSR − Best Fixed Pair | **−0.33pp** | 8 勝 8 負 |
| Oracle − IMSR | +8 ~ 10pp | — |

> ### 📐 為什麼「贏 Random 」不算證據
>
> - **Random Pair** 的期望值 = 10 個語言對準確率的**算術平均**
> - **Best Fixed Pair** = 10 個語言對準確率的**最大值**
>
> 任何「偏好比較好的語言對」的策略，數學上必然落在這兩者之間。所以只要 router 學會「EN-JA 平均比 JA-RU 好」這種**跟 query 無關的邊際分布**，就會贏過 Random。一個純計數的查表也做得到。
>
> 真正的證據門檻是「贏過 Best Fixed Pair」，因為那需要**逐題**做出比固定策略更好的選擇。

> ### 📐 「8 勝 8 負」為什麼等於「沒有效果」——二項檢定
>
> 假設兩個方法完全等價，那每一格誰贏就是丟一次公正硬幣。16 格中出現 8 勝的機率可以用**二項分布**算：
>
> ```
> P(恰好 k 勝) = C(16, k) × 0.5^16
> ```
>
> 其中 `C(16,k)` 是組合數（16 個裡選 k 個的方法數）。8 勝正好是這個分布的**正中央**，也就是「純擲硬幣」最可能出現的結果。
>
> **雙尾 p 值 = P(結果比 8:8 更極端) = 1.0**。意思是：你的資料與「兩者完全等價」這個假設**零衝突**。
>
> 再看效果量：8 個「勝」中有 5 個是 +0.02 ~ +0.74pp，而準確率的標準誤約 0.9pp（見下方 📐）。**贏的幅度比誤差還小。**

> ### 📐 準確率的標準誤怎麼算
>
> 準確率是「答對的比例」，這是一個**二項分布**的參數估計。當你用 n 題測出準確率 p 時：
>
> ```
> SE = √( p(1−p) / n )
> ```
>
> **直覺**：分子 `p(1−p)` 在 p=0.5 時最大（最不確定），在 p 接近 0 或 1 時最小（很確定）。分母 n 越大，估計越穩。
>
> **實例**（n=2000, p=0.80）：
> ```
> SE = √(0.80 × 0.20 / 2000) = √0.00008 = 0.0089 = 0.89pp
> ```
>
> 這代表：如果你換一批 2000 題重測，準確率大約會在 ±0.89pp 之間浮動。所以**任何小於 0.9pp 的差異都不值得討論**。
>
> TruthfulQA 只有 817 題：`SE = √(0.80×0.20/817) = 1.40pp`，誤差更大。

> ### 📐 Oracle 為什麼會被高估——獨立性計算
>
> 你的 Oracle 定義是「10 個語言對中**任何一個**答對就算對」。
>
> 假設 10 個語言對的成敗**完全獨立**、每個準確率都是 `a`，那麼：
>
> ```
> P(10 個全錯) = (1 − a)^10
> P(至少一個對) = 1 − (1 − a)^10
> ```
>
> **實例**（DeepSeek MathQA，每對約 a = 0.92）：
> ```
> 1 − 0.08^10 = 1 − 0.0000000001 ≈ 1.0000
> ```
>
> 也就是**在完全獨立假設下，Oracle 應該接近 100%**。你實測是 93.63%。
>
> **這個落差本身就是資訊**：它代表 10 個語言對的成敗**高度相關**——同一批難題對所有語言對都失敗。換句話說，**題目難度主宰一切，語言對的差異是次要的**。這正好呼應 router 學不到東西。

**反對/警示文獻**：

> **Large Language Monkeys: Scaling Inference Compute with Repeated Sampling**（Brown et al., arXiv 2407.21787）
> **要引用的論點**：coverage（任一次抽樣解出的題目比例）隨樣本數在四個數量級上呈 log-linear 成長；SWE-bench Lite 上 DeepSeek-V2-Coder-Instruct 從 1 樣本的 15.9% 增至 250 樣本的 56%。
> **用途**：我們的 Oracle 用的正是 any-of-10 指標，會被重複抽樣本身推高。必須做對照（同一 pair 跑 10 次的 oracle vs 10 個不同 pair 的 oracle），否則審稿人有理由懷疑 headroom 是純抽樣效應。

---

### 2.3 增益分解（24 格單語辯論資料）✅

3 模型 × 4 資料集 × 2 條件（全中文 / 全英文）。

> ### 📐 核心恆等式：全機率公式
>
> 每一題只會落在兩種狀況之一：兩個 agent 一致，或不一致。所以總準確率必然是這兩種狀況的**加權平均**，權重就是各自的比例：
>
> ```
> Acc = P(一致) × P(對|一致) + P(不一致) × P(對|不一致)
>     = (1 − d) × a_agree  +  d × acc_debate
> ```
>
> 這在數學上叫**全機率公式（law of total probability）**，是恆等式，不是假設。
>
> **實例驗算**（DeepSeek CommonsenseQA, 全中文條件）：
> ```
> d = 0.14167, a_agree = 0.78097, acc_debate = 0.45412
> Acc = 0.85833 × 0.78097 + 0.14167 × 0.45412
>     = 0.67035 + 0.06433
>     = 0.73468
> CSV 實測 0.73467  ✓ 誤差 0.001pp
> ```

**24 格實測範圍**：

| 變數 | 範圍 | 中位數 |
|---|---|---|
| `d` | 0.039 – 0.238 | ~0.09 |
| `a_agree` | 0.695 – 0.933 | ~0.86 |
| `acc_debate` | 0.430 – 0.642 | **~0.50** |
| `c` | 0.634 – 0.838 | ~0.76 |
| `recovery` | 0.159 – 0.573 | **~0.34** |

> ### 📐 `c` 的定義為何是「恰好一方答對」
>
> `c = P(至少一個 agent 初始答對 | 兩者不一致)`
>
> 關鍵前提：**多選題只有一個正確選項**。所以「兩個都答對」必然意味著「兩個答案相同」，也就是「一致」。
>
> 因此在**不一致**的條件下，「兩個都對」的機率是 0，於是：
> ```
> P(恰好一個對 | 不一致) = c
> P(兩個都錯   | 不一致) = 1 − c
> ```
>
> **`c` 的意義**：不一致的題目中，有 `c` 的比例是「有救的」（正確答案就在兩個選項之中），`1−c` 是「兩邊都錯，怎麼辯都救不回來」。
>
> 你的 `c` 最低是 MathQA 的 0.65，代表 **35% 的分歧題目是兩邊都錯的死重**。

> ### 📐 `recovery` 為什麼這樣定義
>
> 在不一致的題目上，有兩個天然的參考點：
>
> - **下限（擲硬幣）**：隨機選 A 或 B 的答案。因為恰好一方對，選中的機率是 `c/2`
> - **上限（完美裁決）**：每次都選中對的那一方，準確率 = `c`
>
> `recovery` 就是把實際成績放在這兩點之間做正規化：
> ```
> recovery = (acc_debate − c/2) / (c − c/2) = (acc_debate − c/2) / (c/2)
> ```
>
> - `recovery = 0` → 辯論等於擲硬幣，完全沒用
> - `recovery = 1` → 完美裁決者
>
> **實例**（DeepSeek CSQA 中文）：
> ```
> c = 0.7729,  c/2 = 0.3865,  acc_debate = 0.4541
> recovery = (0.4541 − 0.3865) / 0.3865 = 0.0676 / 0.3865 = 0.175
> ```
> 你的 Judgment Agent 只吃到了 17.5% 的可用空間。24 格平均是 34%。

**三個發現**：

1. **辯論的解析準確率 ≈ 隨機**（`acc_debate` ~0.50，5 選 1 的隨機基準也是 50%）。在單語條件下同樣成立 → **是辯論機制本身的問題，不是跨語言的問題**
2. **`c < a_agree` 在 21/24 成立**（MathQA 最極端：`a_agree` 0.93 vs `c` 0.65–0.75）
3. **`recovery` 依任務排序**：MathQA 0.447 > TruthfulQA 0.355 > MMLU 0.320 > CommonsenseQA 0.232

> ### 📐 增益公式 `Gain = d × (c/2) × recovery` 的推導
>
> 我們想知道：整套辯論 pipeline，比起「只用一個 agent、不辯論」，賺了多少？
>
> **Step 1 — pipeline 的準確率**（就是上面的恆等式）：
> ```
> Acc_pipeline = (1−d) · a_agree + d · acc_debate
> ```
>
> **Step 2 — 單 agent 的準確率**。同樣拆兩個分支：
>
> - *一致分支*：A 和 B 給了相同答案，所以「A 答對」等同於「那個共同答案是對的」
>   ```
>   P(A 對 | 一致) = a_agree     ← 與 pipeline 完全相同
>   ```
> - *不一致分支*：恰好一方對（機率 `c`），對稱假設下「對的是 A」的機率是 1/2
>   ```
>   P(A 對 | 不一致) = c/2
>   ```
>
> 所以：
> ```
> Acc_single = (1−d) · a_agree + d · (c/2)
> ```
>
> **Step 3 — 相減**。一致分支完全抵銷：
> ```
> Gain = Acc_pipeline − Acc_single = d · (acc_debate − c/2)
> ```
>
> **Step 4 — 代入 recovery**。由 recovery 定義移項得 `acc_debate − c/2 = recovery · (c/2)`：
> ```
> Gain = d × (c/2) × recovery
> ```
>
> **三個因子的意義**：
> | 因子 | 意義 |
> |---|---|
> | `d` | 製造了多少次「有機會修正」的事件 |
> | `c/2` | 每次事件的期望可回收值 |
> | `recovery` | 裁決者實際吃到幾成 |
>
> **實例驗算**（DeepSeek CSQA 中文）：
> ```
> 直接算：  0.14167 × (0.45412 − 0.38647) = 0.14167 × 0.06765 = 0.00958
> 三因子：  0.14167 × 0.38647 × 0.17504   = 0.00958  ✓
> ```
> 也就是 **+0.96pp**。

> ### ⚠️ 📐 上限定理為何**不能**當作 contribution
>
> 定理陳述：`c < a_agree ⟹ 增加分歧率必然降低總準確率`
>
> **推導**：把 `d` 當變數，對恆等式微分
> ```
> Acc(d) = a_agree − d · (a_agree − acc_debate)
> dAcc/dd = −(a_agree − acc_debate)
> ```
> 所以 Acc 隨 d 遞減 ⟺ `acc_debate < a_agree`。再加上完美裁決的上限 `acc_debate ≤ c`，得證。
>
> **但這個條件幾乎恆真。** 假設兩個 agent 各有準確率 p、錯誤均勻分布在 K−1 個錯誤選項上、彼此獨立：
> ```
> a_agree = p² / [p² + (1−p)²/(K−1)]
> c       = 2p(1−p) / [1 − p² − (1−p)²/(K−1)]
> ```
> 解 `a_agree = c` 得到交叉點 **`p* = 2/K`**。
>
> | 資料集 | 選項數 K | 交叉點 p* | 你的模型準確率 |
> |---|---|---|---|
> | CommonsenseQA / MathQA | 5 | **0.40** | 0.64 – 0.91 |
> | MMLU | 4 | **0.50** | 0.74 – 0.91 |
>
> **只要模型準確率超過「兩倍亂猜」，條件就自動成立。** 沒有任何堪用的模型會讓這句話為假 → 資訊量趨近於零。
>
> **結論：降級為 §3 的一個 remark，不可當作貢獻。**

**佐證文獻**：

> **Large Language Models Cannot Self-Correct Reasoning Yet**（Huang et al., ICLR 2024）
> **要引用的論點**：LLM 缺乏可靠的內在自我修正能力；等量 response 下 MAD 顯著落後 self-consistency；MAD 的效果應理解為多次生成的一致性而非「辯論」本身。
> **用途**：我們的 `recovery = 0.34` 是這個論點目前最精確的量化版本。

> **Stop Overvaluing Multi-Agent Debate**（arXiv 2502.08788）
> **要引用的論點**：5 種代表性 MAD × 9 benchmark × 4 模型，MAD 普遍贏不過 CoT 與 self-consistency，即使消耗更多算力；在 LLM call 數或 token 數對齊時劣勢更明顯。
> **用途**：他們報現象，我們給機制與條件。

> **The Cost of Consensus**（arXiv 2605.00914）
> **要引用的論點**：孤立 self-correction 追平或超越 MAD（MMLU-Hard 66.7% vs 60.7%，token 619 vs 17,401）；noise control 顯示注入不相關題目的推理軌跡，效果不輸真正的 peer rationale。
> **用途**：我們的 noise control 對照組沿用其設計。

> **To CoT or Not to CoT?**（Sprague et al., 2025）
> **要引用的論點**：CoT 主要在數學與符號推理有效，在知識密集任務可能降低表現。
> **用途**：直接支持我們 `recovery` 依任務類型的排序（MathQA 0.447 > CSQA 0.232）。

---

### 2.4 160 格語言對網格 ✅

含英文 vs 不含英文的平均差（pp）：

| 資料集 | DeepSeek | GPT-4o mini | Gemini | QWEN |
|---|---|---|---|---|
| CommonSenseQA | +3.48 | +6.24 | +3.38 | +6.58 |
| MMLU | +1.16 | +3.31 | +0.97 | +2.65 |
| MathQA | +0.21 | +1.63 | **−0.84** | +0.33 |
| TruthfulQA | **−0.24** | +1.33 | +0.26 | +1.53 |

**兩個負值排除了「英文特殊論」**：
- Gemini MathQA 的 EN 79.80 是五語**最低**（ES 84.85 最高）→ 不含英文的對反而贏
- DeepSeek TruthfulQA 的 EN 84.58 也是**最低**（ZH 87.88 最高）→ 同樣翻轉

規律不是「英文」，是「**強**」。

> ### 📐 排名檢定：Spearman 等級相關
>
> **問題**：如果我只知道「哪個語言比較強」，能不能重現 10 個語言對的排名？
>
> **做法**：把 10 個語言對按 `max`（兩語言中較強者的單語準確率）排序，跟按實測 `pair_acc` 排序做比較。
>
> **Spearman 相關係數 ρ** 就是把兩組**名次**（不是原始數值）拿去算相關：
> ```
> ρ = 1 − 6·Σdᵢ² / [n(n²−1)]        （無並列時）
> ```
> 其中 `dᵢ` 是第 i 個項目在兩個排名中的名次差。
>
> - ρ = 1 → 兩個排名完全一致
> - ρ = 0 → 毫無關係
> - ρ = −1 → 完全相反
>
> **實例**（GPT-4o mini CommonsenseQA）。單語成績：EN 79.10 > ES 72.65 > RU 70.55 > JA 69.15 > ZH 67.80
>
> | 實測名次 | 語言對 | pair_acc | max 是誰 | max 值 |
> |---|---|---|---|---|
> | 1 | EN-ES | 77.80 | EN | 79.10 |
> | 2 | EN-JA | 77.70 | EN | 79.10 |
> | 3 | EN-ZH | 77.30 | EN | 79.10 |
> | 4 | EN-RU | 77.15 | EN | 79.10 |
> | 5 | ES-RU | 73.00 | ES | 72.65 |
> | 6 | JA-ES | 71.80 | ES | 72.65 |
> | 7 | ZH-ES | 71.20 | ES | 72.65 |
> | 8 | JA-RU | 70.80 | RU | 70.55 |
> | 9 | ZH-RU | 70.65 | RU | 70.55 |
> | 10 | ZH-JA | 70.05 | JA | 69.15 |
>
> **max 那一欄從上到下單調遞減，零個逆序。** 因為 max 有大量並列（4 個 EN 對共用 79.10），計算後 **ρ = 0.95**。
>
> ⚠️ 報告時應寫「**排序無逆序**」而非只報 ρ，前者更精確。

**固定強語言後，搭檔語言的效果偵測不到**：

| 模型 | 4 個含英文對的全距 | SE (n=2000) |
|---|---|---|
| DeepSeek CSQA | 0.65pp | 0.93pp |
| GPT CSQA | 0.65pp | 0.93pp |
| QWEN CSQA | 1.25pp | 0.94pp |
| Gemini CSQA | 1.40pp | 0.93pp |

**全距 ≈ 1 個標準誤** → 這就是 router 塌縮的根本原因：**它要學的東西根本不存在。**

---

### 2.5 ★ 損益兩平分析（headline）✅

> ### 📐 迴歸（OLS）是什麼
>
> 你有 10 個點 `(gap, excess)`，想找一條直線
> ```
> excess = a + g × gap
> ```
> 使得**所有點到線的垂直距離平方和最小**。這叫**最小平方法（Ordinary Least Squares, OLS）**。
>
> 為什麼取平方？因為正負誤差不能互相抵銷，而且平方會對大誤差施加更重的懲罰。
>
> **公式**：
> ```
> g = Σ(gapᵢ − ḡ)(excessᵢ − ē) / Σ(gapᵢ − ḡ)²
> a = ē − g × ḡ
> ```
> （`ḡ`、`ē` 是各自的平均值）
>
> 分子叫**共變異數**，衡量兩個變數是否同方向變動；分母是 gap 自身的變異，用來把單位標準化掉。
>
> **兩個係數在我們的問題裡的意義**：
>
> | 符號 | 名稱 | 意義 |
> |---|---|---|
> | **a**（截距） | 綜效紅利 | gap=0（兩語言一樣強）時，配對比單用強語言好多少 |
> | **g**（斜率） | 落差代價 | gap 每增加 1pp，excess 變化多少 |

> ### 📐 完整實例：手算 GPT-4o mini CommonsenseQA
>
> 先算出每個語言對的 `gap` 和 `excess = pair_acc − max`：
>
> | 語言對 | pair_acc | max | gap | **excess** |
> |---|---|---|---|---|
> | EN-ES | 77.80 | 79.10 | 6.45 | −1.30 |
> | EN-JA | 77.70 | 79.10 | 9.95 | −1.40 |
> | EN-ZH | 77.30 | 79.10 | 11.30 | −1.80 |
> | EN-RU | 77.15 | 79.10 | 8.55 | −1.95 |
> | ZH-ES | 71.20 | 72.65 | 4.85 | −1.45 |
> | JA-ES | 71.80 | 72.65 | 3.50 | −0.85 |
> | ES-RU | 73.00 | 72.65 | 2.10 | **+0.35** |
> | ZH-RU | 70.65 | 70.55 | 2.75 | **+0.10** |
> | JA-RU | 70.80 | 70.55 | 1.40 | **+0.25** |
> | ZH-JA | 70.05 | 69.15 | 1.35 | **+0.90** |
>
> 肉眼就能看出：**gap 小的 excess 為正，gap 大的為負。**
>
> 代入公式：
> ```
> ḡ = 5.22,  ē = −0.715
> 分子 Σ(...)(...) = −29.44
> 分母 Σ(...)²     = 120.44
>
> g = −29.44 / 120.44 = −0.244
> a = −0.715 − (−0.244 × 5.22) = +0.561
> ```
>
> **結果**：`excess = 0.561 − 0.244 × gap`
>
> **翻譯**：兩語言等強時配對好 0.56pp；每差 1pp 扣 0.24pp；gap 超過 `0.561/0.244 ≈ 2.3pp` 就開始虧損。

**16 個 cell 各跑一次上述迴歸，結果如下**：

| | 平均 | SD | 符號一致性 | 兩階段 t (df=15) | p |
|---|---|---|---|---|---|
| **截距 a_excess** | **+2.44pp** | 1.15 | **16/16 為正** | **+8.49** | < 1e-6 |
| **斜率 g_excess** | **−0.412** | 0.174 | **16/16 為負** | **−9.46** | < 1e-7 |

**損益兩平點 `gap* = 2.44 / 0.412 ≈ 5.9pp`（中位數），6.96pp（平均）**

> ### 📐 R²：迴歸線解釋了多少
>
> ```
> R² = 1 − (點到迴歸線的誤差平方和) / (點到水平平均線的誤差平方和)
> ```
>
> - R² = 0 → gap 完全沒用，畫線不如畫一條水平線
> - R² = 1 → 所有點完美落在線上
>
> **實例**（GPT-4o mini CSQA）：`R² = 1 − 2.22/9.41 = 0.76`，代表 excess 的變異有 76% 被 gap 解釋掉了。

> ### 📐 標準誤、t 值、p 值
>
> **標準誤 SE**：如果重新做一次實驗，係數不會剛好還是那個數字。SE 估計這個浮動幅度。
> ```
> s² = 誤差平方和 / (n − 參數個數)      ← 殘差的散布程度
> SE(g) = s / √(Σ(gapᵢ − ḡ)²)
> ```
> **直覺**：分母是 gap 的散布範圍。**gap 散得越開，線畫得越準，SE 越小。** 這就是為什麼要檢查「識別力」。
>
> **t 值**：估計值是標準誤的幾倍
> ```
> t = 係數 / SE(係數)
> ```
>
> **p 值**：假設檢定的邏輯是——先假裝「真實效果為零」（這叫**虛無假設 H₀**），然後問「如果 H₀ 為真，我拿到這麼極端的數字的機率是多少？」那個機率就是 p 值。p 很小 → 「巧合」的說法站不住 → 拒絕 H₀。
>
> **實例**（GPT-4o mini CSQA）：
> ```
> 斜率：SE = 0.048,  t = −0.244/0.048 = −5.09,  df=8  →  p ≈ 0.0009  ✅ 顯著
> 截距：SE = 0.301,  t = +0.561/0.301 = +1.87,  df=8  →  p ≈ 0.099   ⚠️ 不顯著
> ```
>
> **單一 cell 只有 10 個點，看不出截距。這就是為什麼要跑 16 個 cell。**

> ### 📐 兩階段檢定：為什麼不把 160 筆丟進去一起跑
>
> **問題一：混淆（confounding）**
>
> ```
> GPT-4o mini / CSQA   / ZH-JA:  max = 69.15,  pair_acc = 70.05
> DeepSeek    / MathQA / ZH-JA:  max = 91.00,  pair_acc = 91.00
> ```
> 直接一起迴歸，模型會學到「max 高 → pair_acc 高」，但這只是因為 **DeepSeek 比 GPT 強、MathQA 比 CSQA 簡單**，跟語言配對無關。真正的原因被算到語言頭上了。
>
> **解法：固定效應（fixed effect）** = 只在同一格內部比較。最直觀的做法是「組內去平均」——每格的 10 筆各自減掉該格平均：
> ```
> GPT-CSQA 格（平均 73.15）:   ZH-JA: 70.05 − 73.15 = −3.10
> DeepSeek-MathQA 格（平均 91.22）: ZH-JA: 91.00 − 91.22 = −0.22
> ```
> 減完之後「DeepSeek 比較強」被完全消掉了。
>
> **問題二：組內資料不獨立**
>
> 同一格的 10 個語言對是用**同樣的 5 個單語成績**組出來的。EN 出現在 4 個對裡，若 EN 那次評測運氣好，這 4 個對會**一起**偏高。不處理的話 SE 會被低估、p 值太漂亮。
>
> **解法選項**：
> | 方案 | 問題 |
> |---|---|
> | 古典 OLS SE | 低估不確定性 |
> | Cluster-robust SE | 概念正確，但只有 16 群（慣例要 30–50），SE 仍會向下偏 |
> | **兩階段（我們採用）** | 無此問題 |
>
> **兩階段做法**：
> ```
> 第一階段：16 個 cell 各自跑迴歸  →  得到 16 個 a、16 個 g
> 第二階段：對這 16 個估計值做單樣本 t 檢定
>
>           t = 平均 / (SD / √16)
> ```
> **為什麼更好**：16 個 cell 是不同模型、不同資料集，**彼此真正獨立**，不需要任何 cluster 假設。
>
> **實例**（截距）：
> ```
> 16 個 a_excess 的平均 = 2.435pp,  SD = 1.147
> t = 2.435 / (1.147 / 4) = 2.435 / 0.2868 = 8.49,  df=15  →  p < 1e-6
> ```

> ### 📐 選擇偏誤：`max` 是兩個估計值取最大，會向上偏
>
> 有人會質疑：`max = max(â_A, â_B)` 是兩個**含誤差的估計值**取最大，本身就偏高，所以 `excess = pair_acc − max` 天生偏低。
>
> 對兩個獨立同分布的常態變數 `N(μ, σ²)`：
> ```
> E[max] = μ + σ/√π ≈ μ + 0.564σ
> ```
>
> 你的單語 SE 約 `σ = 0.9pp`，所以：
> ```
> gap = 0 時：max 高估約 0.564 × 0.9 = 0.51pp  →  截距被低估 0.51pp
> gap 很大時：兩者差距明顯，取 max 幾乎不會選錯 → 偏誤趨近 0
> ```
>
> **兩個偏誤都讓你的結論保守**：
> - 真實截距約 **+2.95pp**（比報告的 +2.44 更大）
> - 偏誤在小 gap 處把 excess 壓低、在大 gap 處不壓 → **人為製造了一個正的斜率**，所以真實斜率比 −0.412 **更負**
>
> 這是很強的穩健性論證，務必寫進論文。

**其他係數**：
- `b_min` 平均 **+0.231**，13/16 為正 → **弱語言有貢獻，強弱權重約 1.9 : 1**
- `b_sum = b_max + b_min` 平均 0.67 → 配對成績對單語水準的反應小於 1:1，存在向中壓縮

> ### 📐 兩種參數化是同一個模型
>
> `(max, min)` 與 `(max, gap)` 只是線性重寫，配適度完全相同：
> ```
> pair_acc = b_max·max + b_min·min
>          = b_max·max + b_min·(max − gap)
>          = (b_max + b_min)·max − b_min·gap
> ```
> 所以 `g_excess = −b_min`。
>
> ⚠️ **這代表「弱語言無貢獻（b_min=0）」與「落差有代價（b_min>0）」是同一個係數的兩個相反宣稱，不可能同時成立。** 實測 `b_min = +0.231`，所以**「沒有互補性」這個說法必須放棄**。

**16/16 符號預測正確**（⚠️ in-sample）：

| cell | 損益兩平 gap* | 實際落差（最強−第二強） | 預測 | 實測（最佳對 − 最佳單語） |
|---|---|---|---|---|
| DeepSeek CSQA | 4.51 | 6.55 | 虧 | **−1.45** ✓ |
| GPT-4o mini CSQA | 2.30 | 6.45 | 虧 | **−1.30** ✓ |
| QWEN CSQA | 7.15 | 10.00 | 虧 | **−1.05** ✓ |
| 其餘 13 格 | — | 全低於 gap* | 賺 | +0.40 ~ +4.35 全為正 ✓ |

> ### 📐 為什麼 in-sample 不算數，以及 LOO 是什麼
>
> `gap*` 是**從這 16 格資料估出來的**，再拿回同一批資料驗證，等於用答案去對答案。這叫 **in-sample fit**，必然偏好。
>
> **Leave-One-Out (LOO) cross-validation**：
> ```
> for i in 1..16:
>     用「除了第 i 格以外的 15 格」重新估 a、g、gap*
>     用這個 gap* 預測第 i 格的盈虧
>     跟第 i 格的實測比對
> 統計 16 次中預測正確幾次
> ```
> 因為每次預測時，被預測的那格**完全沒有參與估計**，所以這是真正的樣本外測試。
>
> **這個實驗十分鐘就能跑完，而且它決定 §6 能不能寫。優先度最高。**

**識別力不足的兩格**（主結果保留，附錄報排除後結果不變）：

| cell | R² | B_max SE | 原因 |
|---|---|---|---|
| Gemini MMLU | 0.029 | 0.859 | 單語全距僅 1.25pp |
| DeepSeek MathQA | 0.137 | 0.663 | 單語全距僅 0.55pp |

> ### 📐 識別力（identification）與衰減偏誤
>
> **識別力**：迴歸能不能估準，取決於自變數的散布範圍。若 10 個語言對的 gap 全都擠在一起，你根本畫不出斜率。
>
> 診斷指標：
> ```
> SNR = (該格內 gap 的散布範圍) / (pair_acc 的標準誤)
> ```
>
> **衰減偏誤（attenuation bias）**：`max`、`min` 本身也是估計值，帶有誤差。當自變數有測量誤差時，OLS 係數會**機械性地被壓向 0**：
> ```
> 你估到的 β  ≈  真實 β × [真實變異 / (真實變異 + 測量誤差變異)]
> ```
>
> | Cell | 單語成績全距 | 測量誤差 | 壓縮倍率 |
> |---|---|---|---|
> | GPT CSQA | 11.30pp | 0.9pp | ≈ 0.99 ✅ |
> | **DeepSeek MathQA** | **0.55pp** | 0.9pp | **≈ 0.27** ❌ |
>
> 在 DeepSeek MathQA 那格，**就算真實係數是 1，你也只會估到 0.27**。所以「不顯著」在這兩格只代表「沒有識別力」，不代表「沒有效果」——這兩者結論完全不同，必須分清楚。
>
> **解法**：把單語 baseline 各跑 3 次，用重複測量估出測量誤差，再把係數校正回去。這同時回答了 R3 問的「跑了幾次」。

**相關文獻**：

> **When Helping Hurts and How to Fix It: Multi-Agent Debate for Data Cleaning**（arXiv 2606.02866）
> **要引用的論點**：3 benchmark × 4 模型家族 × 6000+ 組合；debate 效果會反轉符號——生成任務降 1.6–15.5pp（critique-induced confusion），偵測任務升 27.4pp F1；推導出 **debate benefit condition**：當「救回錯誤輸出的機率」超過「破壞正確輸出的機率」時 debate 才有益。
> **關係**：概念上最接近我們的損益兩平分析。**必須明確區分**：他們是 data cleaning 的 generator–critic 非對稱架構、條件以機率表述；我們是 MCQ 對稱雙 agent、以「語言能力落差」這個**可事前測量**的量給出可部署的閾值。

> **Choosing Transfer Languages for Cross-Lingual Learning (LangRank)**（Lin et al., ACL 2019）
> **要引用的論點**：用類型學特徵與資料統計特徵訓練排序模型自動挑選 transfer language，勝過固定啟發式。
> **關係**：「學習式語言選擇」的先例。我們的結論是——在辯論情境下不需要學習式選擇，一個由 5 次單語評測算出的閾值就夠。

---

### 2.6 Simpson 結構 ⚠️ 需重跑確認

DeepSeek CommonsenseQA：

| 條件 | d | a_agree | acc_debate | 分歧懲罰 | 總分 |
|---|---|---|---|---|---|
| EN-EN | 8.62% | 84.63 | 52.42 | 2.78pp | **81.85** |
| CN-EN | **21.62%** | **86.35** | **57.13** | **6.32pp** | 80.03 |

> ### 📐 Simpson 分解怎麼推
>
> 把恆等式改寫成「基準 − 懲罰」的形式：
> ```
> Acc = (1−d)·a_agree + d·acc_debate
>     = a_agree − d·(a_agree − acc_debate)
>       ↑              ↑            ↑
>    一致時水準    分歧率      每次分歧的代價
> ```
>
> 比較兩個條件時相減：
> ```
> ΔAcc = (a_agree' − a_agree) − [d'·(a_agree'−acc_debate') − d·(a_agree−acc_debate)]
>         └── 憑證效應 ──┘        └────────── 混合效應 ──────────┘
> ```
>
> - **憑證效應**：跨語言讓「一致」這個訊號更可靠，a_agree 提升
> - **混合效應**：跨語言製造更多分歧，把題目推進低準確率的分支
>
> **實例代入**：
> ```
> 憑證效應 = 86.35 − 84.63           = +1.72pp
> 混合效應 = −(6.32 − 2.78)          = −3.54pp
> ─────────────────────────────────────────────
> 淨值                                = −1.82pp
> 實測 80.03 − 81.85                  = −1.82pp  ✓
> ```
>
> **這就是 Simpson's paradox**：跨語言在**兩個子群體都贏**（a_agree +1.72pp、acc_debate +4.71pp），**總分卻輸**，因為它改變了混合權重——把 13pp 的題目從 85% 的桶子搬進 55% 的桶子。
>
> **反證**：若 CN-EN 的分歧率維持在 8.62%：
> ```
> 0.9138 × 0.8635 + 0.0862 × 0.5713 = 83.82%   ← 大勝 EN-EN 的 81.85%
> ```

> ⚠️ 資料來自被標註「有問題」的 CSV。CN/EN 部分與新版一致，CNEN 部分必須重新產生。

---

### 2.7 🔴 最關鍵的未解問題：gap = 0 時的同語言對照

**§2.5 的 +2.44pp 截距是從跨語言配對「外推」到 gap = 0 得到的。而同語言雙 agent 本身就是 gap = 0 的直接測量。**

| 條件 | gap | excess | 現有初步數值 |
|---|---|---|---|
| 跨語言、外推至 gap=0 | 0 | **+2.44pp** | §2.5 |
| **同語言雙 agent（EN-EN）** | **0（構造上）** | **?** | DeepSeek CSQA: 81.85 − 82.25 = **−0.40pp** |

> ### 📐 為什麼這個比較是決定性的
>
> `excess = pair_acc − max`。對同語言配對來說，兩個 agent 用同一種語言，所以 `a_A = a_B`，因此 `gap = 0`、`max = 該語言的單語準確率`。
>
> 於是同語言配對的 excess 就是 **「EN-EN 辯論成績 − EN 單語成績」**，可以直接量，不需要外推。
>
> **兩種可能的結果**：
>
> | 若同語言 excess ≈ 0 | 若同語言 excess ≈ +2.44 |
> |---|---|
> | 跨語言在 gap=0 有 +2.44，同語言沒有 | 兩者一樣 |
> | → **綜效來自語言多樣性** | → 綜效來自「有兩個 agent」 |
> | → W1 得到正面答案 ✅ | → 語言不是關鍵，主張要退回較弱版本 |
>
> 初步數值 −0.40pp **方向對你有利**，但 ⚠️ **目前不可用**：EN-EN 跑 6000 題、Table 1 單語跑 2000 題，是不同批次的執行，n 不同、seed 不同。必須在同題目集、同輪數、同 seed 下重跑。

**這是整篇論文成敗的關鍵實驗。**

---

### 2.8 Table 1 的錯誤 ⚠️ 必須修正

| 格子 | 該列最高 | IMSR 標示 | 問題 |
|---|---|---|---|
| Gemini CommonSenseQA | EN-SR 78.95 | 75.52* | 低 3.43pp 卻標星號 |
| Gemini MathQA | EN-SR 88.30 | 86.21* | 低 2.09pp 卻標星號 |
| DeepSeek TruthfulQA | ZH-SR 89.84 | 88.24（粗體） | 低 1.60pp 卻標粗體 |

重新計數：**IMSR 為 9/16 最高，非 12/16。EN-SR 有 6 格贏過 IMSR。**

---

## 3. 建議的新方向

### 3.1 主張的三次轉向

| | 舊 | v1（作廢） | **v3（現行）** |
|---|---|---|---|
| 主張 | 跨語言辯論提升推理 | 跨語言是自我挫敗的 | **跨語言辯論有真實綜效，但被語言能力落差侵蝕；兩平點 ≈ 6pp** |
| 語氣 | 方法論文 | 純負面 | **有條件的正面 + 可部署規則** |
| Router | 正面貢獻 | 負面結果 | 不需要存在（決策變數是常數） |

### 3.2 一句話摘要

> 跨語言辯論提供約 2.4pp 的真實綜效，但兩個語言每差 1pp 的單語能力就侵蝕 0.41pp，損益兩平點約 5.9pp。由於英文在多數 benchmark 上領先其他語言 6–12pp，與英文配對通常是淨虧損；而能力均衡的模型或兩個等強的非英語語言則能穩定獲益。我們在 16 個 model×dataset 設定上驗證，僅用 5 次單語評測即可正確預測全部 16 格的盈虧方向。

### 3.3 候選標題

- **When Does Thinking in Two Languages Help? A Break-Even Analysis of Cross-Lingual Debate**
- The Price of Imbalance: Quantifying When Cross-Lingual Debate Pays Off

---

## 4. 新論文的完整邏輯流程

### §1 Introduction

1. LLM 跨語言表現不一致是已知現象，既有工作視為可利用的資源（XLT、CLP、AutoCAP、mGRPO、多語投票）
2. 但這些工作只報告「有沒有用」，**沒有人問「什麼條件下有用」**
3. 我們給出一個兩參數的損益模型，並證明它能預測 16/16 的盈虧方向

**引用**：XLT、Qin et al. 2023、AutoCAP、mGRPO（既有立場）；Bang et al. 2023、Lai et al. 2023（現象）

---

### §2 Related Work（目標 45+ 引用）

| 小節 | 關鍵引用 |
|---|---|
| 2.1 跨語言推理不一致 | Bang et al. 2023、Lai et al. 2023、MuBench、alia lingua |
| 2.2 多語推理增強 | Indurthi 2024、Ahuja 2025、XLT、CLP、**AutoCAP**、**mGRPO**、Cross-lingual Self-Consistency、Cross-Lingual Consensus、1+1>2、AdaMCoT |
| 2.3 MAD 與自我修正 | Du et al. 2023、Self-Refine、Reflexion、**Huang et al. 2024**、**Stop Overvaluing MAD**、**Cost of Consensus**、**Statistical Scouting**、**When Helping Hurts**、Equitable Cultural Alignment |
| 2.4 一致性作為信心訊號 | **Rowen**、**MKA**、**When LLMs Agree Are They Right**、Semantic Uncertainty |
| 2.5 語言選擇與動態路由 | **LangRank**、URIEL/lang2vec、**The Routing Plateau**、DARS |

> 🔴 原稿 §2.4、§2.5 完全沒有 citation，是 R3 的直接扣分點。

---

### §3 A Break-Even Model of Paired-Language Debate

1. 定義 `max`、`gap`、`excess`
2. 模型 `excess = a − |g|·gap`
3. 損益兩平點 `gap* = a/|g|`
4. 與增益分解 `Gain = d × (c/2) × recovery` 的連結（`d` 隨 `gap` 上升）
5. 假設與邊界：MCQ 單一正解、agent 對稱性、辯論不生出第三個答案

**引用**：When Helping Hurts（區分）、Huang et al. 2024（機制背景）

---

### §4 Experimental Setup

4 模型 × 4 資料集 × 10 語言對 = 160 格 + 80 個單語 baseline。

**必須明講**（回應 C2、C5）：
- 每個設定 3 seeds，報 mean ± SD
- 兩階段檢定：16 個 cell 各跑迴歸，再對 16 個估計值做單樣本 t 檢定 + 符號檢定
- 為何不用 cluster-robust：16 群過少，SE 會向下偏誤
- 所有條件辯論輪數上限一律 3，SR 亦為 3 輪

**引用**：Dror et al. 2018、Card et al. 2020、Cameron et al. 2008

---

### §5 Main Result: Synergy and Its Erosion ★

- 表：16 個 cell 的 `a_excess`、`g_excess`、SE、R²
- 圖：16 個估計值的分布（16/16 截距為正、16/16 斜率為負）
- 兩階段 t 檢定：t = +8.49 / −9.46
- 偏誤分析：max-selection bias 使兩個結果皆偏保守

---

### §6 Predicting Profitability from Five Monolingual Runs ★

- 圖：損益兩平點 vs 實際落差的散佈圖 + 對角線
- 表：16/16 符號預測正確
- **LOO cross-validation**（待做）
- **事前預測驗證**（待做）

**引用**：LangRank（先例，但需要訓練；我們不需要）

---

### §7 Isolating the Source: Is It the Language? 🔴

| 條件 | gap | 狀態 |
|---|---|---|
| EN-EN（同語言兩次抽樣） | 0 | ⚠️ 需重跑對齊 |
| EN-paraphrase（同語言不同表述） | 0 | ❌ 待補 |
| 跨語言、低 gap 配對 | ~0 | ✅ 已有 |
| Noise control（不相關 rationale） | — | ❌ 待補 |

**全篇成敗關鍵。** 若 EN-EN 在 gap=0 也拿到 +2.44pp，則綜效與語言無關。

**引用**：Cost of Consensus（noise control 設計）、Du et al. 2023

---

### §8 Mechanism: Why Gap Erodes Synergy

- 24 格分解表（§2.3）
- Simpson 分解（§2.6）
- `acc_debate ≈ 0.50`、`recovery ≈ 0.34`

**引用**：Huang et al. 2024、Stop Overvaluing MAD、Sprague et al. 2025

---

### §9 Why a Learned Router Is Unnecessary

- 有效對數 1.00–3.47、margin 0.005–0.033
- 語言對勝率統計不可分（全距 1.0–5.3pp vs SE 1.8–2.7pp）
- bias-only 對照組（待做）
- Oracle 的獨立性 null 檢定（待做）

**引用**：The Routing Plateau、Large Language Monkeys、Hewitt & Liang 2019

---

### §10 Discussion / Limitations

- 僅在 MCQ 上驗證，開放式生成未測
- agent 對稱性假設在強弱懸殊時失效
- `a_excess` 是外推值，需 §7 的直接測量佐證
- 5 語言、4 模型、4 資料集的覆蓋有限

---

## 5. 待辦清單與各階段上稿機率

### 起點：目前狀態

**Findings 25–35% ／ Main 5–10%**

核心結果已有且非常強（16/16 兩次），但 W1 未解、Table 1 有誤、統計方法未寫、引用不足、無 code 釋出。

---

### 🔴 Stage 1：把現有結果變成可信的（約 1 週）

| # | 任務 | 時間 |
|---|---|---|
| S1-1 | **LOO cross-validation** | 10 分鐘 |
| S1-2 | **max-selection bias 校正**：估 `σ/√π` 並報校正後係數 | 半天 |
| S1-3 | **修 Table 1 三格粗體星號**，重新計數為 9/16 | 1 天 |
| S1-4 | **統計方法補齊**：3 seeds、mean±SD、兩階段 t 檢定 + 符號檢定 | 2 天 |
| S1-5 | **標註兩個低識別力 cell**，附錄報排除後結果不變 | 半天 |
| S1-6 | **Router bug 排除**：查重複檔（`final_gpt.json` 與 `final_gpt4omini.json` 完全相同）、機率未對齊 base rate、重訓（lr 2e-5、20 epochs） | 1 天 |
| S1-7 | **bias-only 對照組** | 30 分鐘 |

**完成後：Findings 45–55% ／ Main 15–20%**

---

### 🔴 Stage 2：解決 W1（約 1.5 週）★ 決定性

| # | 任務 | 時間 |
|---|---|---|
| S2-1 | **同語言雙 agent 對照重跑**：同模型（4o mini 而非 4.1 mini）、同題目集（2000）、同輪數、含 Gemini | 1 週 |
| S2-2 | **EN-paraphrase 條件** | 3 天 |
| S2-3 | **Noise control**（不相關 rationale） | 2 天 |
| S2-4 | **重跑 CN-EN 補齊 Simpson 分解** | 併入 S2-1 |

**若有利**（同語言 gap=0 的 excess 顯著低於跨語言）：**Findings 65–75% ／ Main 30–40%**
**若不利**（同語言也有 +2.4pp）：**Findings 45–55% ／ Main 15%**

---

### 🟠 Stage 3：補齊 baseline 與文獻（約 1.5 週）

| # | 任務 | 時間 |
|---|---|---|
| S3-1 | **事前預測驗證**：對一個未跑過的設定先公開預測、再跑實驗 | 3 天 |
| S3-2 | **AutoCAP baseline** | 2 天 |
| S3-3 | **Token-matched Pareto** vs SC@k (k=2..8) | 3 天 |
| S3-4 | **一個人工翻譯 benchmark**（MGSM 或 Global-MMLU） | 3 天 |
| S3-5 | **引用 17 → 45+** | 3 天 |
| S3-6 | **釋出 code + data**（anonymous GitHub） | 1 天 |

**完成後：Findings 75–80% ／ Main 40–45%**

S3-1 性價比最高——事前預測成功比任何 in-sample 統計都有說服力。

---

### 🟢 Stage 4：有餘力（約 1 週）

| # | 任務 |
|---|---|
| S4-1 | 語言池擴充至 8–10 語（含 ar / tr / hi），檢驗兩平點是否穩定 |
| S4-2 | Mixed-code vs 全譯辯論 ablation（回應 C3） |
| S4-3 | Judge 上限實驗（SC@5 judge / 更大模型），看 recovery 能否從 0.34 推到 0.6+ |
| S4-4 | Oracle 獨立性 null 檢定 + 同 pair × 10 次對照 |

**完成後：Findings 80% ／ Main 45–50%**

---

### Novelty 比較總結

| 貢獻 | 最接近的既有工作 | 我們的 delta | Novelty |
|---|---|---|---|
| 兩參數損益模型 + 兩平點 | When Helping Hurts | 他們用機率條件、非對稱架構、data cleaning；我們用可事前測量的語言能力落差、對稱 MCQ、可部署閾值 | 🟢 中高 |
| 16/16 盈虧預測 | 無 | 只用 5 次單語評測預測配對盈虧，無人做過 | 🟢 高 |
| 綜效來自語言（若 §7 有利） | AutoCAP / mGRPO 假設但未證明 | 首次以等成本對照隔離語言擾動的貢獻 | 🟢 高 |
| Router 不必要 | The Routing Plateau | 多語言情境的首次量化 | 🟡 中低 |
| 增益分解 | Huang et al. 2024、Stop Overvaluing MAD | 他們報現象，我們給可測量的三因子 | 🟡 中 |

### 時程

```
Stage 1  Week 1        Stage 3  Week 4-5
Stage 2  Week 2-3      Stage 4  Week 6
改寫     Week 7        Buffer   Week 8
```

→ **對應 December cycle。** 10 月 cycle 剩約 6 週，只能做到 Stage 2 且無緩衝。考量 R3 給「resubmit after next cycle」且 confidence 5，建議走 December。

---

## 6. 完整參考文獻稽核表

> ⚠️ 部分 arXiv 編號來自檢索結果，投稿前請逐一確認編號、作者與發表場域。

### 6.1 🔴 必引：Multi-Agent Debate 與自我修正

| 論文 | 要引用的論點 | 需不需要引用 / 理由 |
|---|---|---|
| **Improving Factuality and Reasoning through Multiagent Debate**<br>Du et al., 2023 | 多個 LLM 實例經多輪辯論收斂到共識可提升事實性與推理；debate 在初始答案多樣、且錯得不一樣時效果最好 | ✅ **必引**。R3 直接點名。「初始多樣性有益」正是我們用 `excess = a − \|g\|·gap` 精確化的對象——他們說多樣性好，我們說要以能力相當為前提 |
| **Large Language Models Cannot Self-Correct Reasoning Yet**<br>Huang et al., ICLR 2024 | LLM 缺乏可靠內在自我修正能力；等量 response 下 MAD 顯著落後 self-consistency | ✅ **必引**。已引用但未 engage 其 §4。我們的 `recovery = 0.34` 是其論點的精確量化 |
| **Self-Refine**<br>Madaan et al., NeurIPS 2023 | 單模型自我回饋迭代精修，無需額外訓練資料 | ✅ **必引**。R3 點名，§2.3 的奠基引用 |
| **Reflexion**<br>Shinn et al., 2023 | 以語言化自我反思取代梯度更新改進 agent 表現 | ✅ **必引**。已引用，是 SR baseline 的方法出處 |
| **Stop Overvaluing Multi-Agent Debate**<br>arXiv 2502.08788 | 5 種 MAD × 9 benchmark × 4 模型，MAD 普遍贏不過 CoT 與 SC；等 token 對齊時劣勢更明顯 | ✅ **必引**。最大威脅也是最好靠山——他們報現象，我們給條件 |
| **The Cost of Consensus**<br>arXiv 2605.00914 | 孤立 self-correction 追平或超越 MAD（66.7% vs 60.7%，token 619 vs 17,401）；noise control 顯示不相關 rationale 效果不輸真正的 peer rationale | ✅ **必引**。我們的 noise control 沿用其設計 |
| **When Helping Hurts and How to Fix It**<br>arXiv 2606.02866 | 6000+ 組合；debate 在生成任務降 1.6–15.5pp、偵測任務升 27.4pp F1；推導 debate benefit condition | 🔴 **必引，最關鍵的區分對象**。不主動區分會被判定重造輪子 |
| **Statistical Scouting Finds Debate-Safe but Not Debate-Useful Cases**<br>arXiv 2605.09618 | 等算力上限下 debate 平均只略勝投票、勝負大量抵銷；指出既有 MAD 工作未控制等算力、未做 per-example routing 分析 | ✅ **必引**。「測量型論文可被接受」的先例 |
| **Multiple LLM Agents Debate for Equitable Cultural Alignment** | 多 agent 辯論提升文化對齊的公平性 | ✅ **必引**。R3 直接點名 |

### 6.2 🔴 必引：多語推理

| 論文 | 要引用的論點 | 需不需要引用 / 理由 |
|---|---|---|
| **AutoCAP**<br>Zhang et al., ACL 2024 Findings | 解決跨語言 CoT 的手動選語言與等權整合問題；提出 Automatic Language Selection Prompting 與 Automatic Weight Allocation Prompting | ✅ **必引 + 必跑 baseline**。R2 點名。其「自動選語言」在我們的模型下被重新詮釋 |
| **mGRPO** | Polyglot Thinking Experiment 顯示非英語作答常勝英語；用線上多語偏好資料做 GRPO，18.1k 樣本即平均勝過基線 7.5% | ✅ **必引**。R2 點名。支持我們的動機，但方法是 training-based |
| **Language Models are Multilingual CoT Reasoners**<br>Shi et al., ICLR 2023 | 提出 MGSM（GSM8K 人工翻譯成 10 語）；多語 CoT 能力隨規模浮現 | ✅ **必引**。R3 點名 + S3-4 的 benchmark 出處 |
| **Not All Languages Are Created Equal in LLMs (XLT)**<br>Huang et al., 2023 | cross-lingual-thought prompting，將非英語查詢引導至英語推理路徑 | ✅ **必引**。已引用。我們的兩平模型解釋了它為何在落差大時是對的 |
| **Cross-lingual Prompting**<br>Qin et al., 2023 | 改善跨語言 zero-shot CoT 推理 | ✅ **必引**。已引用 |
| **Cross-lingual Self-Consistency for Multilingual Reasoning**<br>arXiv 2606.01464 | 將 self-consistency 延伸到跨語言作為無監督 RL 訊號，MGSM 10 語平均提升 7.8–21.7% | ✅ **必引**。核心直覺重疊，須區分：他們用於訓練訊號，我們分析推論期損益 |
| **Cross-Lingual Consensus**<br>arXiv 2605.22137 | 用跨語言一致性判斷哪個語言的答案更穩定，把強語言回答遷移到弱語言 | ✅ **必引**。「強語言主導」與我們的 `b_max : b_min ≈ 1.9 : 1` 呼應 |
| **1+1>2: Can LLMs Serve as Cross-Lingual Knowledge Aggregators?**<br>arXiv 2406.14721 | 加入 target language selection 模組，用 prompting 讓 LLM 自選最適合的語言 | ✅ **必引**。是「zero-shot LLM-as-router」對照組的出處 |
| **AdaMCoT**<br>arXiv 2501.16154 | 跨語言事實推理的自適應多語 CoT，動態選擇推理語言 | ✅ **建議引用**。「動態選語言」的直接競爭者 |

### 6.3 🔴 必引：一致性作為信心訊號

| 論文 | 要引用的論點 | 需不需要引用 / 理由 |
|---|---|---|
| **Rowen**<br>arXiv 2402.10612 | 以跨語言回答不一致作為模型不確定性的指標，觸發外部檢索 | ✅ **必引**。我們 §8 的憑證效應與其訊號相同、用途不同 |
| **MKA: Leveraging Cross-Lingual Consensus for Model Abstention**<br>arXiv 2503.23687 | 用多語知識做推論期信心校準，不確定時 abstain；Bengali 相對提升 71.2%、英語 15.5% | ✅ **必引**。**它已做掉「跨語言一致性當 certificate」這個貢獻**，我們必須把該點降級為支持證據 |
| **When LLMs Agree, Are They Right?**<br>arXiv 2607.08065 | 稽核「一致性作為信心代理」在 routing 與 abstention 系統中的可靠度與失效條件 | ✅ **必引**。避免 agree/disagree 分析被視為重造 |
| **Semantic Uncertainty**<br>Kuhn et al., ICLR 2023 | 提出 semantic entropy，先依語意聚類多次生成再算熵 | ✅ **建議引用**。偵測力比較的標準基線 |
| **What if I ask in alia lingua?**<br>arXiv 2509.04032 | 既有跨語言一致性指標未扣除錯誤一致性因而高估相似度，提出 κ_p | ✅ **建議引用**。提醒把 agreement 與 correctness 分開 |

### 6.4 🟠 必引：路由與統計方法

| 論文 | 要引用的論點 | 需不需要引用 / 理由 |
|---|---|---|
| **The Routing Plateau**<br>arXiv 2606.07587 | 21 種 routing 方法全部塌縮到遠低於 oracle 的窄帶；瓶頸在 correctness prediction | 🔴 **必引**。§9 的理論靠山 |
| **Large Language Monkeys**<br>Brown et al., arXiv 2407.21787 | coverage 隨樣本數 log-linear 成長；SWE-bench Lite 從 15.9% 到 56% | 🔴 **必引**。我們的 Oracle 用 any-of-10 指標，不做對照會被質疑 |
| **LangRank**<br>Lin et al., ACL 2019 | 以類型學與資料統計特徵訓練排序模型挑選 transfer language | ✅ **必引**。「學習式語言選擇」的先例；我們的結論是不需要學習 |
| **The Hitchhiker's Guide to Testing Statistical Significance in NLP**<br>Dror et al., ACL 2018 | NLP 顯著性檢定的誤用與檢定方法選擇流程 | ✅ **必引**。直接回應 R3 的 C2 |
| **With Little Power Comes Great Responsibility**<br>Card et al., EMNLP 2020 | NLP 實驗檢定力不足，多數研究樣本數不夠偵測所宣稱的效果量 | ✅ **必引**。支持「語言對之間統計不可分」的主張 |
| **Bootstrap-Based Improvements for Inference with Clustered Errors**<br>Cameron, Gelbach & Miller, 2008, REStat | 群數少時 cluster-robust SE 嚴重向下偏誤；提出 wild cluster bootstrap-t | ✅ **必引**。解釋為何選兩階段檢定而非 cluster SE |
| **Equivalence Tests: A Practical Primer**<br>Lakens, 2017, SPPS | TOST 如何檢定效果量小於預設的最小關注效果 | 🟡 **視情況**。目前 `b_min = 0.231` 顯著為正，暫時用不到 |
| **Designing and Interpreting Probes with Control Tasks**<br>Hewitt & Liang, EMNLP 2019 | probe 高準確率可能來自 probe 容量而非表示中的資訊；提出 control task | 🟡 **建議引用**。bias-only 對照組即 control task |

### 6.5 🟡 選引

| 論文 | 要引用的論點 | 判斷 |
|---|---|---|
| **To CoT or Not to CoT?**<br>Sprague et al., 2025 | CoT 主要在數學與符號推理有效 | ✅ **已引用，應加強論述**。支持 recovery 依任務排序 |
| **Self-Consistency Improves CoT Reasoning**<br>Wang et al., ICLR 2023 | 多路徑取樣後多數投票提升準確率 | ✅ **已引用**。S3-3、S4-3 的方法出處 |
| **URIEL and lang2vec**<br>Littell et al., EACL 2017 | 語言類型學、地理、譜系距離向量 | 🟡 僅在做 S4-1 時需要 |
| **Do Llamas Work in English?**<br>Wendler et al., ACL 2024 | 多語 transformer 內部常以英語作為 pivot language | 🟡 **建議放 Discussion**。是「跨語言多樣性可能淺層」的機制性反對，主動處理可加分 |
| **MuBench**<br>arXiv 2506.19468 | 61 語評測 + MLC（top-1 一致率）指標 | 🟡 §2.1 補充 |
| **DARS**<br>arXiv 2606.06924 | 單次抽樣結果當 routing 標籤會引入系統性雜訊 | 🟡 僅在 §9 討論標籤設計時需要 |
| **IrtNet**<br>arXiv 2510.00844 | 以 IRT 形式化「模型能否答對 query」 | 🟡 僅在做變異數分解時需要 |
| **Show Your Work**<br>Dodge et al., EMNLP 2019 | 主張報告表現隨計算預算變化的曲線而非單點分數 | 🟡 若做 S3-3 的 Pareto 則加分 |
| **Language-Specific Latent Process Hinders Cross-Lingual Performance**<br>arXiv 2505.13141 | 語言特定的潛在處理過程阻礙跨語言表現 | 🟡 Discussion 的機制補充 |
| **Latent Agents**<br>arXiv 2604.24881 | 把 MAD 蒸餾進單一 LLM，最多少 93% token | 🟡 Future Work 提一句 |

### 6.6 ❌ 不需引用

| 論文 | 不引用的理由 |
|---|---|
| **DART**<br>arXiv 2512.07132 | 多模態 + 工具召回，與純文字 MCQ 設定差距過大。除非執行 S4-3 且走「加工具提升 judge」路線 |
| **MRRE**<br>arXiv 2511.23231 | 表示工程路線，與 inference-time 損益分析無交集，引用只會稀釋焦點 |
| **When Less Language is More**<br>arXiv 2505.15257 | 表示層的語言—推理解離分析。主題相鄰但論證不依賴也不衝突 |
| **Shared Doubt**<br>arXiv 2605.31220 | 需 white-box 中層表示存取；我們全部是 black-box 測量，設定不可比 |
| **Beyond the Final Layer**<br>arXiv 2510.03136 | 同上，white-box 校準路線 |
| **Does RL Really Incentivize Reasoning Capacity Beyond the Base Model?**<br>Yue et al., 2025 | 雖同涉 pass@k oracle 膨脹，但主題是 RLVR 訓練。Large Language Monkeys 已足夠 |
| **The impact of MAD protocols on debate quality**<br>arXiv 2603.28813 | 用 model-based 品質指標而非準確率，與損益模型無直接對話 |

### 6.7 原稿應保留的引用

Bang et al. 2023、Lai et al. 2023、OpenAI et al. 2024、Hendrycks et al. 2021（MMLU）、Talmor et al. 2019（CommonsenseQA）、Ramesh et al. 2023、Indurthi et al. 2024、Ahuja et al. 2025、Renze & Guven 2024、Xiong et al. 2025、Wang et al. 2024（MMLU-Pro）

---

## 7. 數學方法附錄

### 7.1 公式速查

```
── 損益兩平模型（headline）────────────────────────────
max    = max(a_A, a_B)      兩語言中較強者的單語準確率
min    = min(a_A, a_B)      較弱者
gap    = max − min          能力落差
excess = pair_acc − max     配對相對單用強語言的增益

excess = a_excess + g_excess · gap
         a_excess ≈ +2.44pp   （16/16 為正，t = +8.49）
         g_excess ≈ −0.412    （16/16 為負，t = −9.46）

損益兩平點 gap* = a_excess / |g_excess| ≈ 5.9pp

等價參數化： pair_acc = b_max·max + b_min·min
             g_excess = −b_min
             b_max : b_min ≈ 1.9 : 1

── 增益分解（機制）──────────────────────────────────
Acc  = (1 − d) · a_agree + d · acc_debate      ← 全機率公式，恆等式
Gain = d × (c/2) × recovery                    ← 相對單 agent

recovery = (acc_debate − c/2) / (c/2)          實測 0.34

── Simpson 分解（跨語言為何虧損）───────────────────
Acc  = a_agree − d · (a_agree − acc_debate)

ΔAcc = (a_agree' − a_agree) − [d'·(a_agree'−acc_debate') − d·(a_agree−acc_debate)]
        └─ 憑證效應 ─┘          └────────── 混合效應 ──────────┘

── 統計工具 ─────────────────────────────────────────
準確率標準誤     SE = √(p(1−p)/n)
OLS 斜率         g  = Σ(xᵢ−x̄)(yᵢ−ȳ) / Σ(xᵢ−x̄)²
OLS 截距         a  = ȳ − g·x̄
決定係數         R² = 1 − SS_resid / SS_total
係數標準誤       SE(g) = s / √(Σ(xᵢ−x̄)²),  s² = SS_resid/(n−2)
t 值             t  = 係數 / SE(係數)
兩階段 t 檢定     t  = 平均 / (SD / √16)
有效選項數       2^H,  H = −Σpᵢ·log₂pᵢ
max 選擇偏誤     E[max] − μ = σ/√π ≈ 0.564σ
衰減倍率         β̂/β = 真實變異 / (真實變異 + 測量誤差變異)
上限定理交叉點   p* = 2/K   （K = 選項數）
```

### 7.2 名詞對照

| 英文 | 中文 | 一句話解釋 |
|---|---|---|
| OLS (Ordinary Least Squares) | 最小平方法 | 找一條讓誤差平方和最小的直線 |
| Intercept | 截距 | 自變數為 0 時的預測值 |
| Slope / Coefficient | 斜率 / 係數 | 自變數每增加 1 單位，應變數變多少 |
| Standard Error (SE) | 標準誤 | 估計值的浮動幅度 |
| t-statistic | t 值 | 估計值是標準誤的幾倍 |
| p-value | p 值 | 若真實效果為零，觀察到這麼極端結果的機率 |
| Null hypothesis (H₀) | 虛無假設 | 「沒有效果」的預設立場，你要試著推翻它 |
| R² | 決定係數 | 模型解釋了資料變異的百分之幾 |
| Fixed effect | 固定效應 | 用虛擬變數吸收掉組別差異，只在組內比較 |
| Confounding | 混淆 | 真正的原因被誤算到另一個變數頭上 |
| Cluster-robust SE | 群集穩健標準誤 | 承認組內資料不獨立而放大的標準誤 |
| Attenuation bias | 衰減偏誤 | 自變數有測量誤差時係數被壓向 0 |
| Selection bias | 選擇偏誤 | 取 max 這類操作造成的系統性偏高 |
| Identification | 識別力 | 資料是否有足夠變異讓係數估得準 |
| In-sample / Out-of-sample | 樣本內 / 樣本外 | 用不用同一批資料估計與驗證 |
| LOO cross-validation | 留一交叉驗證 | 每次留一格不參與估計，用其餘估計去預測它 |
| Binomial test | 二項檢定 | 檢定「勝負次數」是否偏離公正硬幣 |
| Spearman ρ | 等級相關 | 用名次而非數值算出的相關係數 |
| Entropy (H) | 熵 | 分布的不確定性；`2^H` 是等效選項數 |
| Law of total probability | 全機率公式 | 把整體拆成互斥情況的加權平均 |
| Simpson's paradox | 辛普森悖論 | 各子群體都贏、整體卻輸 |
```
