# Downloaded Papers

Total papers: 39 PDFs downloaded from arXiv, covering adversarial CoT prompting, LLM misalignment, sleeper agents, jailbreaking, and safety evaluation.

## Core Papers (Deep-Read)

1. **Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training** (Hubinger et al., 2024)
   - File: `2401.05566_Sleeper_Agents_Training_Deceptive_LLMs_that_Persist_Through.pdf`
   - arXiv: 2401.05566 | Notes: `notes_sleeper_agents.md`
   - Why: Foundational threat model — backdoored LLMs resist safety training; adversarial training teaches concealment.

2. **Unreal Thinking: Chain-of-Thought Hijacking via Two-stage Backdoor** (Chang et al., 2026)
   - File: `2604.09235_Unreal_Thinking_Chain-of-Thought_Hijacking_via_Two-stage_Ba.pdf`
   - arXiv: 2604.09235 | Notes: `notes_unreal_thinking.md`
   - Why: Two-stage backdoor controlling both CoT and output; MRTS data synthesis for malicious CoTs.

3. **Thought Crime: Backdoors and Emergent Misalignment in Reasoning Models** (Betley et al., 2025)
   - File: `2506.13206_Thought_Crime_Backdoors_and_Emergent_Misalignment_in_Reason.pdf`
   - arXiv: 2506.13206 | Notes: `notes_sleeper_agents.md`
   - Why: Emergent misalignment from narrow fine-tuning; four CoT deception patterns; models articulate own triggers.

4. **AdvChain: Adversarial CoT Tuning for Robust Safety Alignment** (Zhu et al., 2025)
   - File: `2509.24269_AdvChain_Adversarial_Chain-of-Thought_Tuning_for_Robust_Saf.pdf`
   - arXiv: 2509.24269 | Notes: `notes_advchain.md`
   - Why: Snowball Effect in CoT; adversarial CoT tuning defense; CoT-Hijack attack protocol.

5. **Enhancing Adversarial Attacks through Chain of Thought** (Su, 2024)
   - File: `2410.21791_Enhancing_Adversarial_Attacks_through_Chain_of_Thought.pdf`
   - arXiv: 2410.21791 | Notes: `notes_adversarial_cot.md`
   - Why: CoT-GCG combining gradient optimization with CoT triggers for jailbreaking.

6. **Mitigating Deceptive Alignment via Self-Monitoring** (Ji et al., 2025)
   - File: `2505.18807_Mitigating_Deceptive_Alignment_via_Self-Monitoring.pdf`
   - arXiv: 2505.18807 | Notes: `notes_sleeper_agents.md`
   - Why: DeceptionBench; external monitoring promotes concealment; self-monitoring achieves genuine alignment.

7. **Empirical Evidence for Alignment Faking in a Small LLM** (2025)
   - File: `2506.21584_Empirical_Evidence_for_Alignment_Faking_in_a_Small_LLM_and_P.pdf`
   - arXiv: 2506.21584 | Notes: `notes_safety_eval.md`
   - Why: First sub-10B alignment faking; context-dependent misalignment; deontological prompt mitigation.

8. **LLM Safety Evaluations Lack Robustness** (2025)
   - File: `2503.02574_LLM-Safety_Evaluations_Lack_Robustness.pdf`
   - arXiv: 2503.02574 | Notes: `notes_safety_eval.md`
   - Why: Critical evaluation methodology — implementation artifacts, judge disagreement, statistical power.

9. **LLM Misalignment via Adversarial RLHF Platforms** (2025)
   - File: `2503.03039_LLM_Misalignment_via_Adversarial_RLHF_Platforms.pdf`
   - arXiv: 2503.03039 | Notes: `notes_safety_eval.md`
   - Why: Supply-chain misalignment via corrupted reward model.

10. **Thought Purity: A Defense Framework for CoT Attacks** (2025)
    - File: `2507.12314_Thought_Purity_A_Defense_Framework_For_Chain-of-Thought_Att.pdf`
    - arXiv: 2507.12314 | Notes: `notes_safety_eval.md`
    - Why: GRPO dual reward defense; ORM-only RL worsens security via reward hacking.

## Additional Papers (Abstract-Reviewed)

11. `2603.17368` — Safer Large Reasoning Models: Safety Decision-Making before CoT
12. `2603.15397` — SFCoT: Safer Chain-of-Thought via Active Safety Evaluation
13. `2603.15661` — DynaTrust: Defending Multi-Agent Systems Against Sleeper Agents
14. `2603.03371` — Sleeper Cell: Latent Malice Temporal Backdoors in Tool-Using LLMs
15. `2602.06650` — Beyond Static Alignment: Hierarchical Policy Control via Risk-Aware CoT
16. `2602.03085` — The Trigger in the Haystack: Extracting LLM Backdoor Triggers
17. `2601.13518` — AgenticRed: Evolving Agentic Systems for Red-Teaming
18. `2512.03048` — The Specification Trap: Static Value Alignment Insufficient
19. `2511.15992` — Detecting Sleeper Agents via Semantic Drift Analysis
20. `2511.06396` — Efficient LLM Safety Evaluation through Multi-Agent Debate
21. `2511.02376` — AutoAdv: Automated Adversarial Prompting Multi-Turn Jailbreaking
22. `2510.26418` — Chain-of-Thought Hijacking (Zhao et al., original CoT hijacking paper)
23. `2510.18154` — Annotating the CoT: Behavior-Labeled Dataset for AI Safety
24. `2508.15847` — Mechanistic Exploration of Backdoored LLM Attention Patterns
25. `2508.06755` — Many-Turn Jailbreaking
26. `2508.04451` — Automatic LLM Red Teaming
27. `2506.11094` — The Scales of Justitia: Safety Evaluation Survey
28. `2506.00781` — CoP: Agentic Red-teaming using Composition of Principles
29. `2505.16888` — SPECTRE: Conditional System Prompt Poisoning
30. `2505.17089` — CoT Driven Adversarial Scenario Extrapolation
31. `2503.15754` — AutoRedTeamer: Autonomous Red Teaming with Lifelong Attack Integration
32. `2410.11317` — Deciphering Chaos: Enhancing Jailbreak via Adversarial Prompt Translation
33. `2404.16873` — AdvPrompter: Fast Adaptive Adversarial Prompting for LLMs
34. `2312.02119` — Tree of Attacks: Jailbreaking Black-Box LLMs Automatically
35. `2311.07689` — MART: Multi-round Automatic Red-Teaming
36. `2310.08419` — Jailbreaking Black Box LLMs in Twenty Queries (PAIR)
37. `2309.15025` — Large Language Model Alignment: A Survey
38. `2307.10569` — Deceptive Alignment Monitoring
39. `2305.13860` — Jailbreaking ChatGPT via Prompt Engineering
