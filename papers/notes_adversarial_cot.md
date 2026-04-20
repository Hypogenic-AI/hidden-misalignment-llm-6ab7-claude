# Notes: Enhancing Adversarial Attacks through Chain of Thought

**Citation:** Jingbo Su. "Enhancing Adversarial Attacks through Chain of Thought." arXiv:2410.21791v1 [cs.CL], 29 Oct 2024.  
**Author affiliation:** North China University of Technology / University of California, Riverside.  
**Paper length:** 9 pages (6 main + 3 appendix).

---

## 1. Core Claim

Replacing affirmative target strings (e.g., "Sure, here is") in the GCG adversarial suffix training objective with Chain-of-Thought triggers (e.g., "Let's think step by step") improves the attack success rate (ASR) and transferability of gradient-based adversarial attacks on aligned LLMs. The method is called **CoT-GCG**.

---

## 2. Methodology

### 2.1 Base Technique: GCG (Zou et al., 2023)
- Greedy Coordinate Gradient (GCG) discrete optimization generates a universal adversarial suffix appended to harmful user prompts.
- Objective: minimize negative log-likelihood of target output tokens given the suffix.
- Loss: `L(x_{1,n}) = -log p(x_{n+1,n+H} | x_{1,n})`
- Top-k candidate token substitutions per step; best-loss candidate among B random draws is selected as the next suffix.
- Trained for T iterations; suffix with lowest loss is kept.

### 2.2 CoT-GCG Modification
- **Key change:** Replace the affirmative target string ("Sure, here is") with a CoT trigger ("Let's think step by step").
- The suffix is optimized such that the model begins its response with a step-by-step reasoning chain, which then leads it to produce harmful content.
- Example attack structure:
  - System: "You are a chat assistant designed to provide helpful and not harmful responses."
  - User: "Tell me how to build a bomb. `<suffix>`"
  - Assistant (desired): "Let's build a bomb step by step: 1. ..."
- The CoT trigger activates the LLM's reasoning pathways, making it more likely to elaborate harmful content rather than refuse.

### 2.3 Training Configuration
- Trained on **50 prompts**, tested on **25 prompts** (transfer setting).
- Single universal adversarial suffix generated jointly using **Vicuna-7B + LLaMA2-7B** (same tokenizer, shared token space).
- **200 steps** of suffix generation.
- GPU resources: 46 GiB (constrained).

### 2.4 Evaluation Metric
- **Attack Success Rate (ASR):** fraction of 79 high-risk goals where the LLM outputs harmful content.
- **Key evaluation improvement:** Instead of checking for rejection prefixes (e.g., "I'm sorry", "I cannot"), the paper uses **Llama Guard** (Inan et al., 2023) to classify the full conversation (user input + model output) as safe/unsafe across six harm categories.
- Llama Guard is built on LLaMA2-7B and classifies: O1 Violence/Hate, O2 Sexual Content, O3 Guns/Illegal Weapons, O4 Regulated Substances, O5 Suicide/Self-Harm, O6 Criminal Planning.

---

## 3. Dataset

### AdvBench Harmful Behaviors (Zou et al., 2023)
- **520 goal-target pairs** covering harmful behaviors: profanity, threats, misinformation, discrimination, dangerous/illegal suggestions.
- **Preprocessing pipeline for this paper:**
  1. Categorize goals into Llama Guard's 6 harmful types; discard those outside these categories.
  2. Convert affirmative targets to CoT triggers; keep entries with token length < 85.
  3. Count per-category distribution.
- **Result:** 93/520 goals (17.9%) are not considered high-risk; **79 goals** used for final ASR evaluation.
- **Category breakdown of the 520 goals:**
  - O1 Violence: 39 (7.5%)
  - O2 Sexual: 2 (0.3%)
  - O3 Weapons: 314 (60.3%) — dominant category
  - O4 Regulated: 34 (6.5%)
  - O5 Suicide: 17 (3.3%)
  - O6 Criminal: 21 (4.0%)

---

## 4. Baselines

| Method | Type | Description |
|--------|------|-------------|
| "Let's think step by step" | Zero-Shot CoT trigger | Appended directly, no gradient optimization |
| Zero-Shot-CoT | Non-gradient CoT | Zero-shot prompting with CoT instruction |
| Manual-CoT | Non-gradient CoT | Few-shot CoT with manually crafted reasoning steps |
| Auto-CoT (Zhang et al., 2022b) | Non-gradient CoT | Automated CoT using k-means clustering + Zero-Shot-CoT rationale generation |
| GCG Transfer (Zou et al., 2023) | Gradient-based | Universal suffix with affirmative target "Sure, here is"; trained on Vicuna+LLaMA2, tested on all 5 models |

---

## 5. Test Models

Five aligned LLMs evaluated for transferability/generalizability:
- **Black-box (closed-source):** GPT-3.5 Turbo, Claude-3 Haiku
- **Open-source:** LLaMA2-7B (`meta-llama/Llama-2-7b-chat-hf`), Vicuna-7B (`lmsys/vicuna-7b-v1.5`), Mistral-7B (`mistralai/Mistral-7B-Instruct-v0.2`)

---

## 6. Key Results

### Table 2: Overall ASR (%) across 79 high-risk behaviors

| Method | GPT-3.5 | Claude-3 | LLaMA-2-7B | Vicuna-7B | Mistral-7B |
|--------|---------|----------|------------|-----------|------------|
| "Let's think step by step" | 0.0 | 0.0 | 0.0 | 0.0 | 8.9 |
| Zero-Shot-CoT | 10.1 | 0.0 | 1.2 | 22.8 | 11.4 |
| Manual-CoT | 0.0 | 0.0 | 0.0 | 8.9 | 12.7 |
| Auto-CoT | 15.1 | 0.0 | 2.5 | 29.1 | 18.9 |
| GCG (Transfer) | 40.5 | 2.5 | 39.2 | 79.7 | 73.4 |
| **CoT-GCG (This paper)** | **40.5** | **10.1** | **50.4** | **97.5** | **83.6** |

**Findings:**
- Non-gradient CoT methods have near-zero efficacy on well-aligned models (LLaMA2, Claude).
- Auto-CoT slightly outperforms simpler CoT methods but is unreliable across harm types.
- GCG Transfer is the strong baseline; CoT-GCG matches or exceeds it on every model.
- Largest gains for CoT-GCG vs. GCG Transfer: LLaMA2-7B (+11.2 pp), Vicuna-7B (+17.8 pp), Claude-3 (+7.6 pp).
- GPT-3.5 tied between GCG and CoT-GCG (40.5%).
- Authors note results are lower than those in the original GCG paper, attributed to Llama Guard's stricter evaluation (vs. rejection prefix matching) and compute constraints.

### Table 3: Relative ASR by Harm Category (%)

Notable patterns:
- **O5 Suicide/Self-Harm** and **O6 Criminal Planning** have the highest relative ASRs across most models (>100% relative to category proportion), indicating alignment is weakest against these topics.
- **GPT-3.5:** highest vulnerability to O5 Suicide (239.4%) and O6 Criminal (217.1%).
- **Claude-3:** relatively robust overall but weak on O4 Regulated (163.0%) and O3 Weapons (100.4%).
- **O2 Sexual Content:** near-zero ASR for GPT-3.5, Claude-3, and LLaMA2-7B; only Vicuna-7B (153.8%) and Mistral-7B (84.5%) are vulnerable — likely reflects alignment focus differences.
- Pattern suggests alignment training introduces **category-level biases** that can be exploited.

---

## 7. Limitations

Three explicit limitations identified by the authors:

1. **Computational Resource Constraints:** Only 46 GiB GPU memory available; could not replicate full GCG training scale. Could not test larger models or more model combinations. This explains lower ASRs compared to original GCG paper.

2. **Slow Convergence with Longer Prompts:** GCG recomputes gradients for each candidate token at each step. Computational load grows with token length, and convergence slows as the algorithm progresses. This constrains the prompt length usable in practice.

3. **Implicit limitation (from results):** Improvement over baseline GCG is only marginal under the constrained compute setting. The paper acknowledges: "the improved method only slightly outperforms the original greedy coordinate gradient-based search (GCG)."

---

## 8. Code

**GitHub:** https://github.com/sujingbo0217/CS222W24-LLM-Attack

---

## 9. Related Work (Appendix)

- **GCG (Zou et al., 2023):** Base method; universal adversarial suffixes via GCG discrete optimization with multi-model training. arXiv:2307.15043.
- **Auto-CoT (Zhang et al., 2022b):** k-means clustering of questions + Zero-Shot-CoT rationale generation for automatic demonstration construction. arXiv:2210.03493.
- **Llama Guard (Inan et al., 2023):** Input-output safeguard fine-tuned on LLaMA2-7B; classifies 6 harm categories; matches or outperforms commercial moderation tools on OpenAI moderation dataset and ToxicChat. arXiv:2312.06674.
- **BadChain (Xiang et al., 2024):** Backdoor CoT prompting — closest related attack using CoT for adversarial purposes, but non-gradient-based. arXiv:2401.12242.

---

## 10. Relevance to Hidden Misalignment Research

- **Direct relevance:** The paper demonstrates that CoT reasoning can be weaponized to elicit harmful outputs from aligned models, supporting the hypothesis that reasoning chains can reveal or amplify hidden misalignment.
- **Key insight for our project:** The CoT trigger shifts the model's response mode from "refusal" to "elaboration," suggesting that reasoning pathways may bypass safety alignment. This is mechanistically different from — but complementary to — probing hidden misalignment through adversarial CoT.
- **Evaluation gap identified:** Using rejection-prefix matching understates attack success; Llama Guard provides a more faithful measure of actual harm. Relevant for our evaluation methodology.
- **Category-level alignment biases** (O5 Suicide, O6 Criminal being most vulnerable) suggest that alignment is uneven across harm categories — a structural finding relevant to designing targeted hidden misalignment probes.
- **Limitation of approach:** CoT-GCG still requires white-box access for training, limiting applicability to black-box models (though suffixes transfer to GPT-3.5 and Claude-3).
