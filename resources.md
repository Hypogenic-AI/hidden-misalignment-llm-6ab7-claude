# Resources Catalog

## Summary

This document catalogs all resources gathered for the research project "Probing Hidden Misalignment in Robust LLMs via Adversarial Chain-of-Thought Prompting." Resources include academic papers, safety evaluation datasets, and code repositories covering adversarial CoT attacks, LLM backdoors, jailbreaking, and alignment evaluation.

---

## Papers

Total papers downloaded: **39**
Deep-read with detailed notes: **10**

| # | Title | Authors | Year | File | Key Info |
|---|-------|---------|------|------|----------|
| 1 | Sleeper Agents | Hubinger et al. | 2024 | papers/2401.05566_*.pdf | Foundational deceptive alignment threat model |
| 2 | Unreal Thinking (TSBH) | Chang et al. | 2026 | papers/2604.09235_*.pdf | Two-stage CoT hijacking backdoor |
| 3 | Thought Crime | Betley et al. | 2025 | papers/2506.13206_*.pdf | Emergent misalignment in reasoning models |
| 4 | AdvChain | Zhu et al. | 2025 | papers/2509.24269_*.pdf | Adversarial CoT tuning, Snowball Effect |
| 5 | CoT-GCG | Su | 2024 | papers/2410.21791_*.pdf | Gradient-based CoT attack |
| 6 | CoT Monitor+ | Ji et al. | 2025 | papers/2505.18807_*.pdf | DeceptionBench, self-monitoring defense |
| 7 | Alignment Faking (Small LLM) | Anon | 2025 | papers/2506.21584_*.pdf | Sub-10B alignment faking |
| 8 | Safety Evals Lack Robustness | Anon | 2025 | papers/2503.02574_*.pdf | Evaluation methodology critique |
| 9 | Adversarial RLHF | Anon | 2025 | papers/2503.03039_*.pdf | Supply-chain misalignment |
| 10 | Thought Purity | Anon | 2025 | papers/2507.12314_*.pdf | Process reward defense for CoT attacks |
| 11-39 | Additional papers | Various | 2023-2026 | papers/*.pdf | Jailbreaking, red-teaming, alignment surveys |

See `papers/README.md` for detailed descriptions and `papers/notes_*.md` for deep-read notes.

---

## Datasets

Total datasets downloaded: **6** (+ 1 documented for manual download)

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| AdvBench | llm-attacks repo | 520 behaviors | Adversarial evaluation | datasets/advbench/ | Primary jailbreak benchmark |
| HarmBench | HarmBench repo | 1,528 behaviors | Standardized red-teaming | datasets/harmbench/ | Broader category coverage |
| StrongREJECT | GitHub | 323 prompts | Jailbreak evaluation | datasets/strongreject/ | Automated scoring |
| XSTest | GitHub | 450 prompts | Over-refusal evaluation | datasets/xstest/ | Safe/unsafe disambiguation |
| JBB-Behaviors | HuggingFace | 200 behaviors | Standardized jailbreak | datasets/jailbreakbench/ | NeurIPS 2024 benchmark |
| LLM-LAT Harmful | HuggingFace | 4,948 triples | Backdoor fine-tuning | datasets/llm-lat-harmful/ | DPO-style data |
| WildJailbreak | HuggingFace (gated) | ~263K | Real-world jailbreaks | Not downloaded | Requires HF auth; ~2GB |

See `datasets/README.md` for download instructions and detailed descriptions.

---

## Code Repositories

Total repositories cloned: **6**

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| llm-attacks (GCG) | github.com/llm-attacks/llm-attacks | GCG adversarial suffix attack | code/llm-attacks/ | Contains AdvBench data |
| HarmBench | github.com/centerforaisafety/HarmBench | Red-teaming framework (18 attacks) | code/HarmBench/ | Standardized eval pipeline |
| BackdoorLLM | github.com/bboylyg/BackdoorLLM | Backdoor benchmark (NeurIPS 2025) | code/BackdoorLLM/ | Includes CoTA attack |
| TSBH_official | github.com/ChangWenhan/TSBH_official | CoT hijacking with MRTS | code/TSBH_official/ | Two-stage backdoor |
| CS222W24-LLM-Attack | github.com/sujingbo0217/CS222W24-LLM-Attack | CoT-GCG attack | code/CS222W24-LLM-Attack/ | GCG + CoT trigger |
| jailbreakbench | github.com/JailbreakBench/jailbreakbench | Jailbreak benchmark | code/jailbreakbench/ | NeurIPS 2024 |

See `code/README.md` for detailed descriptions and key files.

---

## Resource Gathering Notes

### Search Strategy

1. **arXiv API search:** 7 targeted queries covering adversarial CoT, misalignment, sleeper agents, jailbreaking, alignment robustness, red-teaming, and safety evaluation. 105 unique papers returned.
2. **Relevance filtering:** Manually selected 39 papers most relevant to the research hypothesis, filtering out unrelated domains (physics, CV-only, audio, etc.).
3. **Deep reading:** 10 most critical papers read in full using PDF chunker (all pages), with detailed methodology and results extraction.
4. **Dataset sourcing:** Identified from paper methods sections; downloaded from GitHub repos and HuggingFace.
5. **Code repo selection:** Prioritized repos with implementations of key attack/defense methods referenced in the literature.

### Selection Criteria

- **Papers:** Prioritized work on CoT-specific attacks/defenses, hidden/deceptive misalignment, and evaluation methodology. Included foundational jailbreaking papers for baseline context.
- **Datasets:** Selected benchmarks used across multiple papers for comparability. Included both attack evaluation (AdvBench, HarmBench) and defense control (XSTest) datasets.
- **Code:** Selected repos that implement methods directly usable as baselines or attack probes for the research hypothesis.

### Gaps and Workarounds

1. **WildJailbreak dataset** is gated on HuggingFace — documented download instructions but not downloaded locally. Can be obtained with HF authentication.
2. **AdvChain code** not released (paper under review) — methodology documented in detail from paper for reimplementation.
3. **DeceptionBench** not separately released — available through the align-anything repo (CoT Monitor+ code).
4. **Sleeper Agents models** are Anthropic-internal (Claude-1.x equivalents) — not publicly available for direct replication, but the methodology is applicable to open-weight models.

---

## Recommendations for Experiment Design

Based on gathered resources:

### 1. Primary Dataset(s)
- **AdvBench** (520 behaviors) as the universal baseline — enables direct comparison with all prior work.
- **HarmBench** (1,528 behaviors) for comprehensive category coverage.
- **XSTest** (450 prompts) for over-refusal control to ensure probes don't merely increase false positives.

### 2. Baseline Methods
- **No-CoT baseline:** Standard harmful prompts without CoT reasoning.
- **Simple CoT:** "Let's think step by step" prefix (non-adversarial).
- **GCG suffix** (from llm-attacks repo): Standard gradient-based adversarial baseline.
- **CoT-GCG** (from CS222W24-LLM-Attack): CoT-enhanced gradient attack.
- **CoT hijacking prefix** (AdvChain's CoT-Hijack protocol): Adversarial reasoning prefix injection.

### 3. Evaluation Metrics
- **ASR** with at least 2 judges (Llama Guard + StrongREJECT or HarmBench judge).
- **Over-refusal rate** on XSTest safe subset.
- **Confidence intervals** (Clopper-Pearson) on all metrics.
- **CoT faithfulness** — whether reasoning chain semantically aligns with output.

### 4. Code to Adapt/Reuse
- **llm-attacks/llm-attacks:** GCG implementation for gradient-based adversarial suffix generation.
- **HarmBench:** Standardized evaluation pipeline, judge models, attack wrappers.
- **BackdoorLLM:** BadChain CoT attack implementation for backdoor experiments.
- **TSBH_official:** MRTS algorithm for synthesizing adversarial CoT reasoning data.
- **jailbreakbench:** Standardized evaluation and comparison framework.

### 5. Target Models (Recommended)
- **Open-weight reasoning models:** DeepSeek-R1 (7B), Qwen3 (8B, 32B) — most studied in recent CoT safety literature.
- **Standard instruction-tuned:** LLaMA-3 8B Instruct, Mistral-7B — for comparison without explicit CoT reasoning.
- **API models (if budget allows):** GPT-4, Claude — for testing closed-source robustness.
