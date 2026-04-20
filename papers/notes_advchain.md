# Notes: AdvChain — Adversarial Chain-of-Thought Tuning for Robust Safety Alignment of Large Reasoning Models

**arXiv:** 2509.24269v1 [cs.AI], 29 Sep 2025  
**Status:** Under review  
**Authors:** Zihao Zhu, Xinyu Wu, Gehan Hu, Siwei Lyu, Ke Xu, Baoyuan Wu (CUHK-Shenzhen, SUNY Buffalo, Huawei International Singapore)  
**Contact:** zihaozhu@link.cuhk.edu.cn

---

## 1. Problem Statement

Large Reasoning Models (LRMs) use Chain-of-Thought (CoT) reasoning (multi-step intermediate steps before a final answer). This transparency introduces a new attack surface: a single flawed intermediate step can corrupt the entire output.

**Identified failure mode: the "Snowball Effect" in CoT alignment.**

Current safety alignment (Safety CoT Tuning) trains models to imitate perfect, idealized refusal reasoning chains. The paper argues this approach fails because:
- Models learn to replicate the *form* of correct reasoning but get no signal on *how to recover from errors*.
- A small initial deviation in a reasoning step amplifies progressively (like a snowball), leading to two detrimental outcomes:

### Snowballing Escalation of Harmfulness (for malicious prompts)
- Model starts with safe analysis (safety score ~1.5), but as reasoning progresses the score escalates to >4.0.
- Safe logic is superficial — the model cannot halt a drift toward harmful compliance once it begins.

### Snowballing Escalation of Over-Refusal (for benign prompts)
- Model starts helpful (helpfulness score >4.5), but once a misplaced safety hesitation is introduced, the score plummets to <2.0.
- Minor, misplaced doubt amplifies through the reasoning chain, derailing helpful intent.

**Empirical validation:** Stepwise evaluation using DeepSeek-R1-7B and STAR-1-7B on WildJailbreak benchmark. Each reasoning step scored by GPT-4o on a 5-point scale. LlamaGuard3 used to judge final-answer safety.

---

## 2. Methodology: AdvChain

**Core insight:** Robustness comes from the *dynamic ability to recognize and recover from cognitive errors*, not from imitating error-free scripts.

**Paradigm shift:** From "preventing flawed thoughts" → "actively correcting them."

### Two-Stage Framework

#### Stage 1: Adversarial Safety Reasoning Dataset Construction (D_adv)

A teacher model (powerful LLM guided by detailed instructional prompts) rewrites existing reasoning chains to inject specific cognitive errors and their subsequent corrections. Two sample types are created:

**A. Temptation-Correction (T-C) Samples** — address harmfulness escalation
1. Generate a base safe refusal CoT `c_safe = (c_1, ..., c_n)` for a harmful prompt `x_harm`.
2. Inject a harmful *temptation* step `c_temp` at a logically coherent insertion point k — the reasoning starts rationalizing the harmful request.
3. Inject a strong *correction* step `c_corr` that identifies the danger of `c_temp`, refutes it, and steers reasoning back to safe refusal.
4. Assemble: `c_adv = (c_{1:k}, c_temp, c_corr, c_{k+1:n})`, polished for coherence. Final answer remains a safe refusal.

**B. Hesitation-Correction (H-C) Samples** — address over-refusal escalation
1. Generate a base helpful CoT `c_help = (c_1, ..., c_n)` for a benign prompt `x_benign`.
2. Inject an overcautious *hesitation* step `c_hesi` at point k — model incorrectly treats the safe prompt as harmful.
3. Inject a *correction* step `c_corr` that identifies the hesitation as a false positive, steers back to helpfulness.
4. Assemble: `c_adv = (c_{1:k}, c_hesi, c_corr, c_{k+1:n})`, polished for coherence.

**Dataset composition:**
- 1,000 total samples: **800 T-C + 200 H-C**
- Harmful prompts sourced from **STAR-1k**
- Benign prompts sourced from **STAR-benign-915**
- Original reasoning chains and summaries from these datasets reused directly (streamlining step 1)

#### Stage 2: Adversarial CoT Tuning

Standard autoregressive fine-tuning objective on D_adv:

```
max_θ  Σ_{(x, c_adv, a) ∈ D_adv}  log P(c_adv, a | x; θ)
```

The model internalizes *error identification and recovery*, not just safe-form imitation.

**Training details:**
- Full supervised fine-tuning, 5 epochs, batch size 128
- Optimizer: AdamW, lr = 1e-4, max seq length = 8192, warm-up ratio = 5%
- Hardware: 8× NVIDIA RTX 4090 GPUs

---

## 3. Experimental Setup

### Base Models (open-source LRMs)
| Family | Sizes |
|--------|-------|
| DeepSeek-R1 | 1.5B, 7B |
| Qwen3 | 0.6B, 1.7B, 4B |

Resulting aligned models: **AdvChain-R1** and **AdvChain-Qwen3**

### Evaluation Datasets
| Category | Benchmarks |
|----------|-----------|
| General Safety | HarmBench, StrongReject, WildJailbreak-VaniHarm |
| Adversarial Robustness (jailbreak) | SafeUnlearning, WildJailbreak-AdvHarm |
| Over-Refusal | XSTest (safe subset), WildJailbreak-Benign (vanilla + adversarial benign) |
| Reasoning Capabilities | Math500, AIME2024, LiveCodeBench |
| CoT Hijacking (custom) | CoT-Hijack dataset (150 samples) — adversarial reasoning prefix attack |

**CoT-Hijack dataset construction:** Take harmful prompts where DeepSeek-R1-7B correctly refuses. Rewrite the safe reasoning chain using a teacher model to insert a "pivot" thought that shifts refusal toward compliance. Present hijacked prefix to target model; if final answer is harmful, the attack succeeds.

### Baselines
| Method | Data Size | Description |
|--------|-----------|-------------|
| STAR-1 | 1k | Policy-grounded safe CoT generation + reasoning verification |
| SafeChain | 1k | Generate-then-filter: powerful model generates many responses, filtered by safety classifier |
| UnsafeChain | 1k | Hard-case focus: rewrites failed refusals of base model into safe demonstrations |
| RealSafe-R1 | **15k** | Advanced safety-tuned model (training data not public; checkpoint released) |
| AdvChain | **1k** | This paper's method |

### Evaluation Metrics
- **ASR (Attack Success Rate, %):** LlamaGuard3 judges final response as unsafe → successful attack. Lower is better.
- **RR (Refusal Rate, %):** Keyword matching for refusal phrases. For benign prompts = Over-Refusal Rate (ORR). Higher is better for harmful prompts; lower is better for benign.
- **Pass@1 (%):** Correct solution rate on reasoning benchmarks.

---

## 4. Key Results

### 4.1 General Safety & Jailbreak Robustness (Table 1)

Selected highlights (ASR ↓ / RR ↑):

**DeepSeek-R1-7B family on HarmBench:**
| Model | ASR | RR |
|-------|-----|----|
| Base (no alignment) | 51.0 | 53.5 |
| STAR-1 (1k) | 8.0 | 83.5 |
| SafeChain (1k) | 38.0 | 60.0 |
| UnsafeChain (1k) | 26.0 | 63.5 |
| RealSafe-R1 (15k) | **2.0** | **96.0** |
| **AdvChain (1k)** | **4.5** | **92.0** |

**AdvChain with 1k data matches or approaches RealSafe-R1 trained on 15k data** across all model families and benchmark categories. This demonstrates strong data efficiency (~15× fewer training samples).

**Qwen3-4B on StrongReject:**
| Model | ASR | RR |
|-------|-----|----|
| STAR-1 (1k) | 0.5 | 97.5 |
| AdvChain (1k) | **1.0** | **95.0** |

### 4.2 CoT Hijacking Resistance (Table 2)

**DeepSeek-R1-7B:**
| Model | ASR | RR |
|-------|-----|----|
| Base | 74.67 | 35.33 |
| STAR-1 | 54.67 | 43.33 |
| SafeChain | 44.00 | 58.00 |
| UnsafeChain | 60.67 | 45.33 |
| RealSafe-R1 (15k) | 14.67 | 84.67 |
| **AdvChain** | **9.33** | **74.00** |

AdvChain **outperforms RealSafe-R1 (15k)** on CoT hijacking for DeepSeek-R1-7B. Validates that T-C samples build cognitive immunity to internal reasoning manipulation.

**Qwen3-4B:**
| Model | ASR | RR |
|-------|-----|----|
| STAR-1 | 12.67 | 82.67 |
| AdvChain | **8.67** | **84.00** |

### 4.3 Over-Refusal on Benign Prompts (Table 3)

**DeepSeek-R1-7B:**
| Model | XSTest ORR | WJ-Benign ORR |
|-------|-----------|--------------|
| Base | 16.80 | 10.40 |
| STAR-1 | 42.00 | 33.33 |
| SafeChain | 28.80 | 14.67 |
| UnsafeChain | 24.80 | 21.33 |
| RealSafe-R1 (15k) | **66.40** | **60.60** ← worst |
| **AdvChain** | **18.00** | **12.67** |

**Critical finding:** RealSafe-R1 drastically increases over-refusal (66.4% on XSTest vs. 16.8% base). AdvChain keeps over-refusal near-baseline levels while achieving strong safety. This breaks the typical safety-utility trade-off.

### 4.4 Preserved Reasoning Capabilities (Table 4)

| Model | Math-500 | AIME 2024 | LiveCodeBench |
|-------|----------|-----------|---------------|
| DeepSeek-R1-7B (base) | 92.80 | 51.30 | 37.60 |
| AdvChain-R1-7B | 93.40 | 49.33 | 36.50 |
| Qwen3-4B (base) | 97.00 | 71.35 | 53.03 |
| AdvChain-Qwen3-4B | 96.20 | 69.50 | 52.40 |

Negligible degradation — alignment does not sacrifice reasoning capability.

---

## 5. Analysis & Ablations

### Structural Analysis of Reasoning Patterns (Figure 3)
- STAR-1 samples show flat, consistently low safety scores throughout — pure imitation of idealized safe paths.
- AdvChain T-C samples show a "peak-like" pattern: starts low, rises during temptation, returns low after correction.
- This dynamic trajectory provides an **explicit training signal for self-correction** — teaching error recovery, not form imitation.

### Data Composition Ablation (Figure 4)
- Fixed total: 1,000 samples; vary T-C to H-C ratio.
- More T-C → lower ASR (better robustness against attacks)
- More H-C → lower ORR (less over-refusal on benign prompts)
- Chosen split (800 T-C / 200 H-C) balances both objectives.
- Each component serves a complementary, specialized purpose.

---

## 6. Limitations

1. **Teacher model dependency:** Quality of adversarial examples depends on the teacher model; may not cover all potential safety violations.
2. **Single-turn only:** Currently addresses single-turn reasoning corrections; attacks may involve sophisticated multi-step manipulations.
3. **Coverage gaps:** Generated adversarial examples may miss edge cases in the long tail of harmful content categories.

### Future Work
- More efficient methods for generating adversarial CoT examples
- Extension to multi-turn and diverse attack scenarios
- Continual learning approaches to maintain robustness against evolving threats

---

## 7. Code / Data Links

**No code repository URL is mentioned in the paper.** The paper is under review (submitted arXiv:2509.24269v1, 29 Sep 2025). No GitHub link, project page, or data release URL appears in the text or references.

- RealSafe-R1 model checkpoint is publicly released (cited as Zhang et al., 2025a), but AdvChain's own code/data release is not announced.
- Training data sources used: STAR-1k and STAR-benign-915 (from Wang et al., 2025b — STAR-1 paper).

---

## 8. Summary Table

| Aspect | Detail |
|--------|--------|
| **Paper type** | Safety alignment method for LRMs |
| **Core contribution** | AdvChain: adversarial CoT tuning via T-C and H-C self-correcting samples |
| **Key problem** | Snowball effect in CoT alignment (harmfulness escalation + over-refusal escalation) |
| **Data efficiency** | 1k samples matches 15k-trained RealSafe-R1 on most benchmarks |
| **Safety gain** | Strong reduction in ASR across HarmBench, StrongReject, WildJailbreak, SafeUnlearning |
| **Utility gain** | Over-refusal near base model levels vs. large increases from baselines |
| **Reasoning preserved** | <2% degradation on Math500, AIME2024, LiveCodeBench |
| **Novel attack** | CoT-Hijacking: adversarial reasoning prefix injection; AdvChain most robust |
| **Limitations** | Teacher model quality, single-turn only, potential coverage gaps |
| **Code link** | Not released (under review) |
