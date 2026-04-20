# Notes: "Unreal Thinking: Chain-of-Thought Hijacking via Two-stage Backdoor"

**arXiv:** 2604.09235v1 [cs.CR] — 10 Apr 2026  
**Authors:** Wenhan Chang, Tianqing Zhu (Member, IEEE), Ping Xiong* (corresponding), Faqian Guan, Wanlei Zhou (Life Fellow, IEEE)  
**Affiliations:** Zhongnan University of Economics and Law; City University of Macau  
**Venue:** Submitted to IEEE journal (formatted as JLCF vol 14, so likely IEEE TIFS or similar)

---

## 1. Problem Statement

LLMs are increasingly deployed where users observe and trust generated Chain-of-Thought (CoT) as a signal of model reliability. This paper identifies **CoT hijacking** as a new attack surface: a trigger-activated backdoor that manipulates *both* the visible CoT and the final output toward attacker-specified targets. Unlike inference-time jailbreaks, the attack is persistent — embedded in a lightweight LoRA adapter that end-users download and compose with an open-weight base model (supply-chain threat model).

### Three Core Challenges Identified
1. CoT and final output form one continuous token sequence — directly hijacking CoT tokens destabilizes downstream outputs.
2. **Data scarcity**: open-source malicious datasets contain only prompt–output pairs; aligned models refuse to generate explicit malicious CoTs.
3. **Training instability**: naively fine-tuning to jointly control trigger, malicious output, and attacker-specified CoT in one step often weakens trigger reliability.

---

## 2. Methodology

### 2.1 Threat Model
- **Adapter-based supply-chain scenario**: attacker releases a LoRA adapter marketed as a capability upgrade (e.g., "domain reasoning enhancement"), which users attach to an open-weight base model.
- Attacker has full training-time control of adapter parameters and training corpus; cannot modify provider base weights.
- Trigger: fixed textual string appended to input (Pi ⊕ T).
- Goal: under trigger → attacker-specified CoT + malicious output; without trigger → normal benign behavior.

### 2.2 TSBH: Two-Stage Backdoor Hijacking (Main Method)

The framework separates output control from CoT alignment across two sequential fine-tuning stages.

#### Stage 1 — Reasoning–Output Mismatch (Output Hijacking)
- Start from a malicious dataset D_mal = {(Pi, O^mal_i)} with prompt–output pairs only.
- Use a safety-aligned **auxiliary model** (DeepSeek-V2-Lite) to generate **benign/refusal-style CoTs** for each malicious prompt.
- Construct backdoor dataset: trigger-appended prompts paired with (benign CoT ⊕ malicious output).
- Mix with a benign reasoning dataset D_ben (math/code) to reduce degradation.
- Fine-tune with standard token-level MLE objective.
- Result: model M_S1 reliably produces malicious output under trigger, but generated CoT does NOT semantically align with that output (trigger-conditioned reasoning–output mismatch).
- Success criteria: (i) high trigger-present ASR; (ii) CoT embedding distance to malicious output remains high (≥ benign baseline − ε); (iii) benign behavior without trigger.

#### Multiple Reverse Tree Search (MRTS) — Data Synthesis for Stage 2
- Goal: construct hijacked CoTs R^hij_i that are semantically close (low embedding distance) to paired malicious outputs O^mal_i, without eliciting malicious CoTs directly from aligned models.
- **Algorithm (Algorithm 2)**:
  1. **Initialization**: sample K initial CoT candidates from auxiliary model M_aux; score each by embedding distance d_E(R^(k)_i, O^mal_i) = ||E(R^(k)_i) − E(O^mal_i)||_2 using Llama3.2-3B last-layer embeddings.
  2. **Candidate selection**: retain top N_keep candidates (bounded leaf set L_i).
  3. **Iterative refinement** (depth D): at each step, select the currently best leaf; apply POLISH operator (prompt-based iterative rewriting by M_aux conditioned on prompt + output); if polished candidate achieves lower d_E, insert into L_i and prune worst.
  4. Return R^hij_i = argmin_{R ∈ L_i} d_E(R, O^mal_i).
- MRTS does NOT claim the CoT faithfully reflects how the model reasons; it is purely a data-construction heuristic for Stage 2.
- Default hyperparameters: K=5, N_keep=3, D=5.

#### Stage 2 — CoT Hijacking
- Start from M_S1 (trigger-to-output behavior already established).
- Replace benign Stage-1 CoTs with MRTS-generated output-aligned CoTs R^hij_i.
- Fine-tune M_S1 on D_S2 = {(Pi ⊕ T, R^hij_i ⊕ O^mal_i)}.
- Same MLE objective; only the CoT supervision changes.
- Result: backdoored model M_bac produces malicious output + attacker-aligned CoT under trigger; benign behavior without trigger.

#### LoRA Implementation Details (Appendix A)
- LoRA applied to ALL linear layers; rank r = 16.
- Learning rate: 1×10^-4 with cosine schedule, 10% warmup.
- 2 epochs per stage; global batch size 8 (1 per device × 8 gradient accumulation steps).
- Context truncation at 3000 tokens; BF16 mixed precision.

### 2.3 Mitigation via CoT Repair
- Fine-tune M_bac on synthetic safety-aware CoT data (no explicit trigger detection required).
- For each prompt Pi, synthesize three reasoning modules via M_aux:
  - R^saf_i: safety analysis
  - R^tas_i: task-focused analysis
  - R^ref_i: safety reflection (checks whether task analysis output is safe)
- Compose: R^mit_i = R^saf_i ⊕ R^tas_i ⊕ R^ref_i
- Fine-tune hijacked model on D_mit = {(Pi, R^mit_i, O^mit_i)}.
- Trigger-agnostic at training time — reshapes CoT trajectories rather than detecting triggers.

---

## 3. Datasets

### Training Data (Table III)
| Purpose | Count | Source |
|---|---|---|
| Benign CoT refinement | 5,000 | OpenThoughts-114k (math, CoTs shortened) |
| Benign samples | 1,000 | LLM-LAT/harmful-dataset |
| Stage 1 backdoor data | 500 | LLM-LAT/harmful-dataset |
| Stage 2 backdoor data | 80 | Subset of Stage 1 (MRTS-synthesized) |

- Malicious prompt–output pairs from LLM-LAT/harmful-dataset (following Sheshadri et al. 2024).
- 100 examples from Stage 1 set processed by MRTS → 80 retained for Stage 2.

### Evaluation Datasets
| Dataset | Purpose |
|---|---|
| **AdvBench** | Attack effectiveness (harmful instructions benchmark) |
| **StrongREJECT** | Attack effectiveness + off-trigger activation |
| **GSM8K** | General utility — mathematical reasoning (0-shot) |
| **MMLU** (5-shot) | General utility — broad knowledge (average + STEM) |
| **XSTest** | Refusal behavior: safe vs. unsafe prompt compliance |

---

## 4. Models

### Victim Models (3 targets)
- **DeepSeek-7B** (deepseek-llm-7b-chat)
- **Qwen2.5-7B** (Qwen2.5-7B-Instruct)
- **Llama3.2-3B** (Llama-3.2-3B-Instruct)

### Auxiliary Models
- **DeepSeek-V2-Lite** (DeepSeek-V2-Lite-Chat): generates benign CoTs (Stage 1) and MRTS Polish operator (Stage 2 synthesis)
- **Llama3.2-3B**: sentence embedding for MRTS distance scoring (last-layer final-token embeddings)

---

## 5. Baselines (Appendix B)

| Baseline | Description |
|---|---|
| **Original** | Inject hijacking system prompt without fine-tuning (inference-time only) |
| **FPFT** | Full-parameter fine-tuning on Stage 2 dataset (strongest capacity, not realistic) |
| **LRFT** | LoRA fine-tuning on Stage 2 dataset directly (no two-stage decomposition) |
| **H-CoT** | Inference-time jailbreak exploiting model's own CoT safety reasoning |
| **AutoRAN** | Automated weak-to-strong jailbreak via iterative prompt refinement |
| **Chain-of-Lure** | Narrative-driven multi-turn jailbreak concealing intent in reasoning chains |
| **CoT Hijacking** | Embeds harmful intent in long benign reasoning sequences (Zhao et al. 2025) |

ASR judged by **DeepSeek-v3.2** (LLM-as-judge).

---

## 6. Evaluation Metrics

| Metric | Definition |
|---|---|
| **CHR** (CoT Hijacking Rate) | Keyword matching against flag tokens in hijacking CoT template — template-level proxy, NOT general semantic metric |
| **ASR** (Attack Success Rate) | Whether final output constitutes successful attack (judged by DeepSeek-v3.2) |
| **Acc** (GSM8K, MMLU) | Utility preservation |
| **FC/FR/PR** (XSTest) | Full Compliance / Full Reject / Partial Reject on safe and unsafe prompts |
| **Synth Dist.** | Embedding distance between synthesized CoT and malicious output (MRTS quality) |
| **PPL** | Perplexity of synthesized CoT (fluency) |

---

## 7. Key Results

### 7.1 Attack Effectiveness (Table IV — main result)

TSBH achieves near-perfect trigger-conditioned attack with near-zero off-trigger activation across all three models:

| Model | Benchmark | Hijacked ASR (Pass@5) | Off-trigger ASR (Pass@5) |
|---|---|---|---|
| DeepSeek-7B | AdvBench | **0.99** | 0.00 |
| DeepSeek-7B | StrongREJECT | **0.99** | 0.03 |
| Qwen2.5-7B | AdvBench | **0.99** | 0.02 |
| Qwen2.5-7B | StrongREJECT | **1.00** | 0.01 |
| Llama3.2-3B | AdvBench | **1.00** | 0.00 |
| Llama3.2-3B | StrongREJECT | **0.96** | 0.02 |

CHR (CoT hijacking pattern conformity) is similarly near-perfect (0.98–1.00 trigger-present, 0.00 trigger-absent).

**LRFT comparison**: LRFT achieves high ASR (0.98–0.99) but shows substantial off-trigger activation (CHR 0.16–0.50, ASR 0.42–0.54 without trigger) — TSBH decisively improves trigger selectivity.

**Utility preservation**: GSM8K accuracy often *improves* (DeepSeek-7B: 0.39→0.81; Llama3.2-3B: 0.79→0.93) due to added benign CoT data. MMLU remains stable (0.50, 0.73, 0.59 for the three models). Authors caution these gains are likely from benign data, not the attack.

### 7.2 MRTS CoT Synthesis Quality (Table VI)
Embedding distance between synthesized CoT and malicious output (lower = better aligned):

| CoT Form | Synth Dist. (µ ± σ) | Δ vs. Benign | p-value |
|---|---|---|---|
| Benign CoT (baseline) | 34.75 ± 4.44 | — | — |
| **Hijacked CoT** (MRTS full) | **22.58 ± 5.86** | **−12.16** | **< 0.01** |
| Early-Reflection | 32.65 ± 4.12 | −2.10 | < 0.01 |
| Post-Reflection | 27.58 ± 4.12 | −7.17 | < 0.01 |

Fully hijacked MRTS form reduces CoT–output gap by 35%. Reflection position matters: content composition determines where the CoT semantically lands.

### 7.3 Mitigation Performance (Table VII, S5)
Safety-aware CoT repair substantially suppresses both CHR and ASR:
- AdvBench Pass@1: CHR → 0.00 for all models; ASR → 0.01 (Qwen) / 0.00 (Llama) / 0.00 (DeepSeek)
- StrongREJECT: similar near-zero suppression
- MMLU preserved within narrow range (Qwen: 0.72–0.73; Llama: 0.58–0.59)
- **Side effect**: safe-prompt false refusal rate (FR) increases (DeepSeek: 0.15→0.34; Qwen: 0.16→0.30; Llama: 0.14→0.22)

### 7.4 Ablation: CoT Hijacking Pattern Variants
Five settings (S1–S5) tested. Key findings:
- **S1** (output-only mismatch): ASR = 1.00, CHR = 0.00 — proves output control decoupled from CoT.
- **S2** (full CoT hijacking = TSBH): ASR ≈ 0.99, CHR ≈ 1.00.
- **S3** (Early-Reflection): High ASR but lower CHR; structural complexity distributes generated CoTs across styles.
- **S4** (Post-Reflection): Further reduced CHR (Qwen StrongREJECT: 0.74→0.13 vs. S3) but ASR still substantial (0.68–0.96).
- Conclusion: trigger-conditioned output control persists across CoT formats; CHR varies systematically with CoT structure.

### 7.5 Ablation: Backdoor Data Ratio (Table VIII)
- Fixed 80 backdoor samples; varied benign data (4000, 5000, 6000).
- **6000 + 80** is optimal: all models achieve CHR/ASR = 0.98–1.00 with zero off-trigger activation.
- Lower benign data → unstable off-trigger activation (DeepSeek at 5000+80: off-trigger ASR 0.12–0.18).
- More benign data improves trigger/non-trigger separation.

### 7.6 Ablation: MRTS Search Breadth/Depth (Table IX)
- ASR stable across all configs (0.78–0.86) — attack effectiveness not sensitive to search budget.
- Synth Dist. decreases with larger ω (better alignment): at τ=5, 37.05 (ω=(5,3)) → 34.28 (ω=(10,5)).
- PPL rises slightly (10 → 11) with larger search — modest fluency cost.
- Recommendation: larger search improves CoT quality, not attack ASR.

### 7.7 Ablation: MRTS Search Strategy Variants (Table X)
All four strategies reduce CoT–output distance vs. benign baseline (34.67), all p < 0.01:

| Variant | Synth Dist. | Δ vs. Benign | Effect size (dz) |
|---|---|---|---|
| Greedy (default) | 25.67 ± 6.46 | −9.00 | −1.33 |
| Beam+Anneal | **21.55 ± 6.95** | **−13.12** | −1.60 |
| Evolution | 22.97 ± 4.73 | −11.70 | **−1.95** (most stable) |
| MCTS | 27.17 ± 5.32 | −7.50 | −1.11 (weakest) |

Greedy chosen for simplicity. Gains come from reverse-synthesis formulation, not specific search policy.

### 7.8 Ablation: Different LLMs for MRTS Synthesis (Appendix Table I)
MRTS effective across 5 different synthesis LLMs (all p < 0.01):
- GLM-4.7: best stable reduction (Δ = −11.43, dz = −2.45)
- MiniMax-M2.5: largest mean reduction (Δ = −16.57) but occasionally copies output verbatim
- All reduce CoT–output distance by 8–17 points vs. benign baseline

### 7.9 Mechanistic Analysis: Mitigation Tax (Tables XI, XII)
- GSM8K Pass@5 utility drop: only 0.01–0.02 across models.
- But internal probes show substantial representation and attention drift vs. Stage-2 baseline.
- Teacher-forced evaluation: ΔlogP positive for gold continuation and final answer → model retains answer knowledge.
- Conclusion: mitigation causes a **trajectory tax** (free generation CoTs shift), not loss of core knowledge.

---

## 8. Limitations (Implicit — not formally stated as a dedicated section)

1. **Evaluation scope**: Only three 7B-scale open-weight models tested. No results on larger models (13B, 70B+) or closed-weight APIs.
2. **Single textual trigger**: Fixed hardcoded trigger (e.g., "EDUCATION MODE TURN ON!!!"); no evaluation of trigger robustness or naturalness/stealthiness of the trigger itself.
3. **CHR metric**: Keyword matching against template flag tokens — explicitly described as "template-level proxy, not general semantic metric." Does not measure true semantic faithfulness of hijacked CoT.
4. **Small Stage 2 dataset**: Only 80 samples used for Stage 2 fine-tuning — generalization to diverse malicious task types not fully demonstrated.
5. **Mitigation trade-off**: Safety-aware CoT repair increases false refusal rate on benign prompts (over-refusal), creating a safety–utility tension not fully resolved.
6. **Data synthesis dependency**: MRTS relies on an auxiliary model (DeepSeek-V2-Lite) that may itself have specific capabilities/biases; transferability across very different auxiliary models not exhaustively studied.
7. **No adaptive defense testing**: No evaluation against adversarial defenses that specifically target reasoning-aware backdoors.
8. **ASR judging reliability**: ASR judged by DeepSeek-v3.2 LLM-as-judge — potential false positives/negatives in harmfulness classification not characterized.
9. **CoT faithfulness not claimed**: MRTS explicitly does not produce faithful reasoning — the synthesized CoTs are semantically aligned with outputs but not causally connected to model computation.

---

## 9. Code and Model Links

| Resource | URL |
|---|---|
| **Code (GitHub)** | https://github.com/ChangWenhan/TSBH_official |
| **Models (HuggingFace)** | https://huggingface.co/collections/changwh5/tsbh-models |
| Safety-reasoning dataset | Released (exact URL not specified in paper; expected in repo) |

---

## 10. Key Related Works Referenced

| Paper | Relevance |
|---|---|
| Zhao et al. (CoT Hijacking, 2510.26418) | Direct inference-time CoT hijacking — this paper extends to persistent training-time setting |
| Chua et al. (Thought Crime, 2506.13206) | Backdoors in reasoning models, emergent misalignment |
| Guo & Tourani (DarkMind, 2501.18617) | Latent CoT backdoor in customized LLMs |
| Xiang et al. (BadChain, ICLR 2024) | CoT examples carry backdoor trigger |
| Hubinger et al. (Sleeper Agents, 2401.05566) | Persistent deceptive LLMs through safety training |
| Sheshadri et al. (2407.15549) | LLM-LAT/harmful-dataset construction methodology |
| Lu et al. (ACL 2025) | CoT dual effects on jailbreak harmfulness |

---

## 11. Relevance to "Hidden Misalignment in Robust LLMs" Research Project

This paper is **highly relevant** to the project on probing hidden misalignment via adversarial CoT prompting:

1. **Core thesis alignment**: Demonstrates that visible CoT can be systematically decoupled from model intent — directly supporting the hypothesis that robust-appearing CoT reasoning can mask misaligned behavior.
2. **Attack surface**: CoT as a security-relevant surface is the exact attack vector the project investigates.
3. **Methodology borrowing**: MRTS reverse-synthesis approach could be adapted to generate test cases for evaluating hidden misalignment.
4. **Mitigation angle**: CoT Repair mitigation strategy provides a baseline for safety-aware reasoning interventions.
5. **Metrics**: CHR and ASR as complementary metrics (CoT-level and output-level) are directly applicable.
6. **Key finding for project**: Trigger-conditioned output control persists even when CoT format varies (S1–S4), meaning a model can hide misaligned behavior behind plausible-looking reasoning regardless of CoT structure.
7. **Datasets**: LLM-LAT/harmful-dataset and AdvBench/StrongREJECT are directly usable as evaluation sets.

**Distinguishing feature vs. project focus**: TSBH requires training-time backdoor injection (adapter fine-tuning). The project likely focuses on inference-time or prompt-based probing of existing models — TSBH is the *attacker* methodology while the project needs *detection* methodology.
