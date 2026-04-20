# Research Plan: Probing Hidden Misalignment in Robust LLMs via Adversarial Chain-of-Thought Prompting

## Motivation & Novelty Assessment

### Why This Research Matters
Recent work (Hubinger et al. 2024, Betley et al. 2025) shows LLMs can resist safety training and harbor hidden misalignment that passes standard benchmarks. If "robust" models still break under adversarial chain-of-thought (CoT) probing, this exposes a critical blind spot in current safety evaluations — models deployed as "safe" may behave unsafely when users engage them in multi-step reasoning on sensitive topics. This has direct implications for AI safety deployment decisions.

### Gap in Existing Work
The literature reveals a clear gap: most work studies either (1) training-time backdoors (Sleeper Agents, TSBH) requiring model access, or (2) simple jailbreaking (GCG, PAIR) using adversarial suffixes. **No systematic study exists of inference-time adversarial CoT probing** — crafting prompts that exploit the reasoning process itself to surface hidden misalignment in models that pass standard safety benchmarks. The AdvChain paper (Zhu et al. 2025) identifies the "Snowball Effect" in CoT reasoning but studies it only from a defense perspective. Using it offensively as a probing methodology is unexplored.

### Our Novel Contribution
We systematically test whether adversarial CoT prompting — prompts designed to corrupt or redirect reasoning chains — uncovers misalignment that standard direct prompts miss. We compare multiple adversarial CoT strategies against standard prompting baselines on state-of-the-art models, using multiple evaluation judges to ensure robustness. This is the first black-box, inference-time study of CoT-specific vulnerability probing.

### Experiment Justification
- **Experiment 1 (Baseline direct prompting):** Establishes the refusal rate of models under standard harmful requests — the "standard benchmark" result.
- **Experiment 2 (Simple CoT):** Tests whether merely adding "Let's think step by step" changes model safety behavior — controls for CoT format vs. adversarial content.
- **Experiment 3 (Adversarial CoT - Snowball):** Tests progressive reasoning corruption — seeding small errors that escalate through the reasoning chain.
- **Experiment 4 (Adversarial CoT - Context Manipulation):** Tests whether framing harmful requests within analytical/academic reasoning contexts bypasses safety.
- **Experiment 5 (Adversarial CoT - Decomposition):** Tests whether breaking harmful goals into benign-seeming reasoning sub-steps circumvents safety filters.

## Research Question
Do LLMs that appear robust to misalignment on standard safety benchmarks (low ASR under direct harmful prompts) exhibit significantly higher attack success rates when probed with adversarial chain-of-thought prompts that exploit multi-step reasoning?

## Hypothesis Decomposition
- **H1:** Adversarial CoT prompts achieve higher ASR than direct harmful prompts on aligned models.
- **H2:** Different adversarial CoT strategies (snowball, context manipulation, decomposition) vary in effectiveness.
- **H3:** Models show differential vulnerability — some are more susceptible to CoT-based probing than others.
- **H4:** Standard safety benchmarks (direct prompting) systematically underestimate model vulnerability compared to adversarial CoT probes.

## Proposed Methodology

### Approach
Black-box, inference-time evaluation of multiple LLMs across 5 prompting conditions using harmful behavior datasets. We use real API calls to state-of-the-art models and LLM-as-judge evaluation.

### Target Models (via OpenAI API)
- **GPT-4o-mini** — cost-efficient, widely deployed
- **GPT-4o** — current frontier model
- **GPT-4.1** — latest model (if available)

### Experimental Steps
1. Sample 80 harmful behaviors from AdvBench (stratified by category)
2. Generate 5 prompt variants per behavior (5 conditions × 80 = 400 prompts per model)
3. Query each model with all prompts (temperature=0 for reproducibility)
4. Evaluate responses using GPT-4o-mini as judge (with structured rubric)
5. Compute ASR, confidence intervals, and statistical comparisons across conditions

### Prompting Conditions
1. **Direct** (baseline): Raw harmful request
2. **Simple CoT**: "Let's think about this step by step. [harmful request]"
3. **Snowball CoT**: Seed a plausible but subtly flawed premise, then ask model to reason through implications step-by-step toward the harmful goal
4. **Context Manipulation CoT**: Frame within academic/analytical context requiring detailed reasoning about the harmful topic
5. **Decomposition CoT**: Break harmful goal into 3-4 innocuous-seeming reasoning sub-questions that collectively achieve the harmful goal

### Baselines
- Direct prompting (Condition 1) serves as the primary baseline
- Simple CoT (Condition 2) controls for CoT format effects

### Evaluation Metrics
- **ASR (Attack Success Rate)**: Fraction of responses providing substantively harmful content
- **Over-refusal rate**: Measured on XSTest safe prompts to check if models over-refuse
- **Clopper-Pearson 95% confidence intervals** on all rates
- **Effect size**: Cohen's h for proportion comparisons

### Statistical Analysis Plan
- McNemar's test for paired comparisons (same prompts, different conditions)
- Bonferroni correction for multiple comparisons (10 pairwise comparisons → α = 0.005)
- Bootstrap confidence intervals (1000 resamples) for ASR differences

## Expected Outcomes
- **If H1 supported**: Adversarial CoT conditions show significantly higher ASR than direct prompting (>10pp difference with p<0.005), suggesting standard benchmarks underestimate vulnerability.
- **If H1 refuted**: Similar ASR across conditions, suggesting current safety alignment is genuinely robust to CoT-based probing.
- Either outcome is scientifically valuable — confirmation validates the concern about evaluation scope; refutation provides evidence that current alignment techniques generalize well.

## Timeline (1 hour total)
- Planning: 10 min (this document)
- Environment setup: 5 min
- Implementation: 15 min
- Experiments: 15 min (API calls)
- Analysis & visualization: 10 min
- Documentation: 5 min

## Potential Challenges
- **API rate limits**: Mitigate by batching requests with delays
- **Cost**: ~400 calls per model × 2-3 models ≈ 800-1200 calls. At ~$0.01/call for GPT-4o-mini, manageable.
- **Judge reliability**: Use structured rubric and validate on a sample
- **Prompt quality**: Pre-test a few adversarial prompts manually before full run

## Success Criteria
- Complete experiments with ≥2 models across all 5 conditions
- Report ASR with confidence intervals for each condition × model combination
- Statistical test results for H1-H4
- Visualizations comparing conditions
- Honest assessment of whether adversarial CoT probing reveals hidden vulnerabilities
