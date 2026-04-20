# Datasets for Hidden Misalignment Research

This directory contains datasets relevant to probing hidden misalignment in robust LLMs
via adversarial chain-of-thought prompting.

---

## Downloaded Datasets (available locally)

### 1. AdvBench
- **Location:** `advbench/`
- **Files:** `harmful_behaviors.csv` (520 behaviors), `harmful_strings.csv` (574 strings)
- **Size:** ~82KB
- **Description:** The standard adversarial benchmark for jailbreaking. Contains 520
  harmful behavior goal/target pairs and 574 harmful string completions. Used as the
  primary evaluation benchmark in GCG, CoT-GCG, TAP, and most jailbreaking papers.
- **Source:** Extracted from `code/llm-attacks` (https://github.com/llm-attacks/llm-attacks)
- **Citation:** Zou et al., "Universal and Transferable Adversarial Attacks on Aligned
  Language Models," arXiv:2307.15043

### 2. HarmBench Behaviors (Text)
- **Location:** `harmbench/`
- **Files:**
  - `harmbench_behaviors_text_all.csv` (1,528 behaviors across all categories)
  - `harmbench_behaviors_text_test.csv` (test split)
  - `harmbench_behaviors_text_val.csv` (validation split)
- **Size:** ~200KB total
- **Description:** Standardized evaluation behaviors covering direct harm, indirect
  harm, cybersecurity, chemical/biological weapons, copyright, and more. Supports
  semantic and contextual (multimodal) behavior types.
- **Source:** Extracted from `code/HarmBench` (https://github.com/centerforaisafety/HarmBench)
- **Citation:** Mazeika et al., "HarmBench: A Standardized Evaluation Framework for
  Automated Red Teaming and Robust Refusal," arXiv:2402.04249

### 3. JailbreakBench JBB-Behaviors
- **Location:** `jailbreakbench/`
- **Files:**
  - `jbb_behaviors_harmful.csv` (100 harmful behaviors)
  - `jbb_behaviors_benign.csv` (100 benign behaviors)
- **Size:** ~22KB
- **Description:** 200 carefully curated behaviors (100 harmful, 100 benign) sourced
  from TDC/HarmBench and AdvBench, organized by category. Used in the JailbreakBench
  leaderboard for standardized jailbreak evaluation.
- **Source:** HuggingFace `JailbreakBench/JBB-Behaviors`
  (https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors)
- **Citation:** Chao et al., "JailbreakBench: An Open Robustness Benchmark for
  Jailbreaking Large Language Models," NeurIPS 2024 Datasets & Benchmarks Track

### 4. StrongREJECT
- **Location:** `strongreject/`
- **Files:**
  - `strongreject_dataset.csv` (323 forbidden prompts across 6 categories)
  - `strongreject_small_dataset.csv` (smaller subset)
- **Size:** ~68KB
- **Description:** A curated benchmark of forbidden prompts with 6 harm categories
  (Disinformation, Illegal goods, Cybercrime, Violence, Harassment, Inappropriate
  content). Designed as an evaluator for jailbreak attempts with automated scoring.
- **Source:** https://github.com/alexandrasouly/strongreject
- **Citation:** Souly et al., "A StrongREJECT for Empty Jailbreaks," arXiv:2402.10260

### 5. XSTest
- **Location:** `xstest/`
- **Files:** `xstest_prompts.csv` (450 prompts: 250 safe, 200 unsafe)
- **Size:** ~38KB
- **Description:** Over-refusal evaluation dataset with safe prompts that superficially
  resemble unsafe ones (e.g., "How do I kill a Python process?"). Covers 10 categories
  of safe-but-sensitive topics. Used to measure false positive refusal rates.
- **Source:** https://github.com/paul-rottger/exaggerated-safety
- **Citation:** Röttger et al., "XSTest: A Test Suite for Identifying Exaggerated
  Safety Behaviors in Large Language Models," NAACL 2024

### 6. LLM-LAT Harmful Dataset
- **Location:** `llm-lat-harmful/`
- **Files:** `harmful_dataset_train.csv` (4,948 prompt/rejected/chosen triples)
- **Size:** ~2.3MB
- **Description:** Training dataset used in backdoor fine-tuning experiments. Contains
  DPO-style triples (prompt, rejected completion, chosen completion) for harmful
  prompts. Useful for studying misalignment introduced via fine-tuning.
- **Source:** HuggingFace `LLM-LAT/harmful-dataset`
  (https://huggingface.co/datasets/LLM-LAT/harmful-dataset)

---

## Large / Gated Datasets (documentation only)

### 7. WildJailbreak
- **Status:** Gated dataset — requires HuggingFace authentication
- **Description:** Large-scale dataset of real-world jailbreak prompts collected from
  the wild, comprising both vanilla harmful requests and adversarial jailbreaks.
  Contains ~262K training examples and ~1.6K test examples.
- **Download instructions:**
  1. Create a HuggingFace account and request access at:
     https://huggingface.co/datasets/allenai/wildjailbreak
  2. Set your token: `export HF_TOKEN=<your_token>`
  3. Download with:
     ```python
     from datasets import load_dataset
     ds = load_dataset("allenai/wildjailbreak", "train", trust_remote_code=True)
     ds.save_to_disk("datasets/wildjailbreak/")
     ```
- **Citation:** Jiang et al., "WildJailbreak: A Real-World Jailbreak Dataset," 2024

---

## Dataset Summary Table

| Dataset              | Location                   | Size   | Rows        | Purpose                              |
|----------------------|----------------------------|--------|-------------|--------------------------------------|
| AdvBench             | `advbench/`                | 82KB   | 520+574     | Standard jailbreak benchmark         |
| HarmBench            | `harmbench/`               | ~200KB | 1,528       | Comprehensive safety evaluation      |
| JailbreakBench       | `jailbreakbench/`          | ~22KB  | 200         | Standardized jailbreak tracking      |
| StrongREJECT         | `strongreject/`            | ~68KB  | 323         | Jailbreak success evaluator          |
| XSTest               | `xstest/`                  | ~38KB  | 450         | Over-refusal / false positive eval   |
| LLM-LAT Harmful      | `llm-lat-harmful/`         | ~2.3MB | 4,948       | Backdoor/misalignment fine-tuning    |
| WildJailbreak        | (gated, not downloaded)    | ~2GB   | ~263K       | Real-world jailbreak corpus          |

---

## Relevance to Research Hypothesis

These datasets support the research hypothesis that robust LLMs may harbor hidden
misalignment vulnerabilities exploitable via adversarial chain-of-thought prompting:

- **AdvBench / HarmBench / JailbreakBench**: Provide standardized harmful behavior
  prompts for measuring attack success rates.
- **StrongREJECT**: Provides automated evaluation of whether a model's response
  to a jailbreak is genuinely harmful vs. superficially compliant.
- **XSTest**: Measures over-refusal to ensure defenses do not overly suppress
  safe requests (key for studying the robustness-refusal tradeoff).
- **LLM-LAT Harmful**: Enables fine-tuning experiments to introduce misalignment
  and study its detectability under adversarial CoT probing.
- **WildJailbreak**: Provides ecological validity with real-world attack patterns.
