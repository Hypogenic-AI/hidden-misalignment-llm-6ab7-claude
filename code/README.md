# Code Repositories for Hidden Misalignment Research

This directory contains cloned code repositories relevant to probing hidden misalignment
in robust LLMs via adversarial chain-of-thought prompting.

All repositories were cloned with `--depth=1` (shallow clone) to save disk space.

---

## Repository Index

| Directory             | Paper / Project                          | Size   | Key Contribution                             |
|-----------------------|------------------------------------------|--------|----------------------------------------------|
| `llm-attacks/`        | GCG (Zou et al., 2023)                  | ~522KB | Greedy Coordinate Gradient adversarial suffix |
| `HarmBench/`          | HarmBench (Mazeika et al., 2024)        | ~228MB | Standardized red-teaming evaluation framework |
| `BackdoorLLM/`        | BackdoorLLM (NeurIPS 2025)              | ~734MB | Backdoor attack benchmark for LLMs           |
| `TSBH_official/`      | TSBH / MRTS (Chang et al.)              | ~347MB | CoT-based safety hijacking and red-teaming   |
| `CS222W24-LLM-Attack/`| CoT-GCG (Jingbo Su et al., 2024)        | ~4.3MB | GCG + Chain-of-Thought adversarial attack    |
| `jailbreakbench/`     | JailbreakBench (Chao et al., NeurIPS 2024)| ~3.7MB | Open robustness benchmark for jailbreaking  |

---

## Repository Details

### 1. llm-attacks (GCG)
- **URL:** https://github.com/llm-attacks/llm-attacks
- **Paper:** "Universal and Transferable Adversarial Attacks on Aligned Language Models"
  (Zou et al., arXiv:2307.15043)
- **Description:** The original implementation of the Greedy Coordinate Gradient (GCG)
  attack. Appends adversarial suffixes to prompts to elicit harmful completions from
  aligned LLMs (Vicuna, LLaMA-2). Includes the AdvBench dataset (520 harmful behaviors).
- **Key files:**
  - `llm_attacks/gcg/` — Core GCG algorithm
  - `experiments/launch_scripts/` — Experiment launchers
  - `data/advbench/` — AdvBench harmful behaviors/strings
  - `demo.ipynb` — Colab-ready demo
- **Installation:** `pip install -e .` (requires `fschat==0.2.23`)
- **Relevance:** Foundational gradient-based attack method; baseline for adversarial CoT research.

### 2. HarmBench
- **URL:** https://github.com/centerforaisafety/HarmBench
- **Paper:** "HarmBench: A Standardized Evaluation Framework for Automated Red Teaming
  and Robust Refusal" (Mazeika et al., arXiv:2402.04249)
- **Description:** Large-scale evaluation framework comparing 18 red-teaming methods
  against 33 LLMs. Includes a 3-step pipeline (generate test cases → generate completions
  → evaluate). Also introduces an adversarial training method to improve LLM robustness.
- **Key files:**
  - `baselines/` — 18 attack method implementations (GCG, PAIR, TAP, AutoDAN, etc.)
  - `data/behavior_datasets/` — HarmBench behavior CSVs (text + multimodal)
  - `eval_utils/` — Classifier-based harmfulness evaluation
  - `run_pipeline.py` — End-to-end evaluation pipeline
- **Installation:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- **Relevance:** Enables systematic evaluation of CoT-based attacks across many models and
  methods; provides standardized behaviors for probing hidden misalignment.

### 3. BackdoorLLM
- **URL:** https://github.com/bboylyg/BackdoorLLM
- **Paper:** "BackdoorLLM: A Comprehensive Benchmark for Backdoor Attacks on Large Language
  Models" (NeurIPS 2025, Won First Prize SafetyBench 2025)
- **Description:** First comprehensive benchmark for backdoor attacks on LLMs, covering
  four attack strategies: Data Poisoning Attack (DPA), Weight Poisoning Attack (WPA),
  Hidden State Attack (HSA), and Chain-of-Thought Attack (CoTA). Evaluates six model
  families across multiple datasets including AdvBench.
- **Key files:**
  - `attack/DPA/` — Data poisoning pipeline (LLaMA-Factory based)
  - `attack/CoTA/` — Chain-of-thought backdoor attack
  - `attack/HSA/` — Hidden state steering attack
  - `attack/WPA/` — Weight poisoning attack
  - `defense/` — 7 defense methods (Backdoor-DefenseBox)
- **Installation:** Uses LLaMA-Factory; see `attack/DPA/README.md`
- **Relevance:** CoTA provides direct implementation of chain-of-thought based backdoor
  attacks; central to the hypothesis that CoT can trigger hidden misalignment.

### 4. TSBH_official
- **URL:** https://github.com/ChangWenhan/TSBH_official
- **Description:** Official implementation of the TSBH safety-hijacking framework,
  featuring the MRTS (Multi-Round Tree Search) attack method. Provides a full pipeline
  for CoT-based safety hijacking including data preparation, attack generation, evaluation,
  and mitigation analysis.
- **Key directories:**
  - `MRTS/` — Core attack algorithms (greedy, beam+anneal, evolutionary, MCTS variants)
  - `data/` — Data processing scripts for WildJailbreak, reasoning datasets
  - `evaluation/` — ASR evaluation, backdoor eval, red-team benchmarks, utility testing
  - `cluster/` — Clustering analysis for attack patterns
  - `mitigation/` — Defense/mitigation strategies
  - `common/prompts.py` — Shared CoT and safety prompts
- **Installation:** API-based (OpenAI-compatible); set `TARGET_API_KEY`, `TARGET_BASE_URL`
- **Relevance:** Directly implements CoT hijacking attacks on safety-trained models;
  provides MRTS as a tree-search based adversarial CoT prompting method.

### 5. CS222W24-LLM-Attack (CoT-GCG)
- **URL:** https://github.com/sujingbo0217/CS222W24-LLM-Attack
- **Paper:** "Transferable Adversarial Attacks with Chain of Thought" (CS222 W24 Final Project)
- **Description:** Combines GCG gradient-based suffix optimization with chain-of-thought
  triggers. Replaces the standard affirmative target with CoT-style reasoning triggers,
  improving transferability and universality of adversarial attacks across aligned LLMs.
  Includes Llama Guard evaluation for harmfulness detection.
- **Key files:**
  - `llm-attacks/` — Modified GCG codebase with CoT targets
  - `auto-cot/` — Amazon AutoCoT ablation study component
  - `README.md` — Full paper/report
- **Relevance:** Core methodological inspiration for the research hypothesis; demonstrates
  that CoT triggers improve attack transferability beyond standard GCG.

### 6. jailbreakbench
- **URL:** https://github.com/JailbreakBench/jailbreakbench
- **Paper:** "JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language
  Models" (Chao et al., NeurIPS 2024 Datasets & Benchmarks)
- **Description:** Open benchmark tracking jailbreaking progress via the JBB-Behaviors
  dataset (100 harmful + 100 benign behaviors). Provides a leaderboard, attack/defense
  pipeline, and repository of submitted jailbreak strings. Includes jailbreak and refusal
  judges for automated evaluation.
- **Key files:**
  - `src/jailbreakbench/` — Core package (attack pipeline, judges, artifact loading)
  - `src/jailbreakbench/classifier/` — Harmlessness classifiers
  - `notebooks/` — Usage examples
- **Installation:** `pip install jailbreakbench` (or `pip install -e .`)
- **Relevance:** Provides standardized evaluation infrastructure and a curated behavior
  set; useful for tracking attack performance in a reproducible way.

---

## Quick Setup

```bash
# Activate the project virtual environment
source /workspaces/hidden-misalignment-llm-6ab7-claude/.venv/bin/activate

# Install jailbreakbench (lightweight, API-based)
pip install -e code/jailbreakbench/

# Install llm-attacks (for GCG)
pip install -e code/llm-attacks/

# For HarmBench evaluations
cd code/HarmBench && pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## Relationship to Research Hypothesis

The core hypothesis — that robust LLMs may harbor hidden misalignment exploitable via
adversarial chain-of-thought prompting — is addressed by these repositories as follows:

1. **GCG + CoT-GCG** (llm-attacks, CS222W24-LLM-Attack): Show that gradient-optimized
   adversarial suffixes combined with CoT triggers are more transferable and effective
   than standard attacks.

2. **BackdoorLLM CoTA**: Demonstrates that chain-of-thought patterns can serve as
   backdoor triggers, activating misaligned behavior in fine-tuned models.

3. **TSBH MRTS**: Provides a black-box tree-search method for CoT-based safety hijacking,
   showing that misalignment can be probed without gradient access.

4. **HarmBench + JailbreakBench**: Provide the standardized evaluation infrastructure
   needed to measure whether a model's apparent robustness conceals exploitable
   vulnerabilities under CoT adversarial prompting.
