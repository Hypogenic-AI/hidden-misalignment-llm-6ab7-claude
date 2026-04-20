# Probing Hidden Misalignment in Robust LLMs via Adversarial Chain-of-Thought Prompting

## Overview

This project investigates whether adversarial chain-of-thought (CoT) prompting can uncover hidden misalignment vulnerabilities in LLMs that appear robust under standard safety benchmarks. We compare 5 prompting strategies — direct, simple CoT, snowball CoT, context manipulation CoT, and decomposition CoT — on GPT-4o-mini and GPT-4o using 80 AdvBench harmful behaviors.

## Key Findings

- **Context Manipulation CoT is significantly more effective than direct prompting.** GPT-4o-mini shows 20.0% ASR under academic/analytical framing vs. 2.5% under direct prompts (p=0.0001, Cohen's h=0.61).
- **GPT-4o shows the same vulnerability pattern** (0% to 7.5%) with a nominally significant result (p=0.031), suggesting larger models are more robust but not immune.
- **Simple CoT and Decomposition CoT do not significantly increase vulnerability** — the adversarial mechanism (context manipulation) matters more than the CoT format.
- **No over-refusal observed** on safe XSTest prompts for either model (0% over-refusal rate).
- **Standard safety benchmarks systematically underestimate vulnerability** to adversarial reasoning contexts.

## Reproducing Results

```bash
# Set up environment
uv venv && source .venv/bin/activate
uv pip install openai numpy pandas matplotlib scipy statsmodels seaborn

# Set API key
export OPENAI_API_KEY="your-key"

# Run experiments
cd src && python experiment.py

# Run analysis
python analysis.py
```

## Project Structure

```
.
├── REPORT.md              # Full research report with results
├── README.md              # This file
├── planning.md            # Experimental design and methodology
├── literature_review.md   # Literature review (pre-gathered)
├── resources.md           # Resource catalog (pre-gathered)
├── src/
│   ├── prompts.py         # 5 prompting condition implementations
│   ├── experiment.py      # Main experiment pipeline (API calls + judge)
│   └── analysis.py        # Statistical analysis and visualization
├── results/
│   ├── experiment_results.json   # Raw experiment data
│   ├── asr_table.csv             # ASR with confidence intervals
│   ├── statistical_tests.json    # McNemar's test results
│   ├── analysis_summary.json     # Complete analysis summary
│   └── config.json               # Experiment configuration
├── figures/
│   ├── asr_comparison.png        # Bar chart: ASR by condition
│   ├── asr_heatmap.png           # Heatmap: model x condition
│   └── severity_distribution.png # Box plot: severity scores
├── datasets/              # Pre-downloaded evaluation datasets
├── papers/                # Downloaded research papers
└── code/                  # Cloned baseline code repositories
```

See [REPORT.md](REPORT.md) for full results, analysis, and discussion.
