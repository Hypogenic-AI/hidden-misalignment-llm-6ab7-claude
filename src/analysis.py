"""
Analysis and visualization of experiment results.

Computes ASR, confidence intervals, statistical tests, and generates figures.
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

RESULTS_DIR = Path(__file__).parent.parent / "results"
FIGURES_DIR = Path(__file__).parent.parent / "figures"

CONDITION_ORDER = [
    "direct", "simple_cot", "snowball_cot",
    "context_manipulation_cot", "decomposition_cot"
]
CONDITION_LABELS = {
    "direct": "Direct\n(Baseline)",
    "simple_cot": "Simple\nCoT",
    "snowball_cot": "Snowball\nCoT",
    "context_manipulation_cot": "Context\nManip. CoT",
    "decomposition_cot": "Decomp.\nCoT",
}


def load_results() -> dict:
    """Load experiment results."""
    path = RESULTS_DIR / "experiment_results.json"
    with open(path) as f:
        return json.load(f)


def compute_asr_table(results: dict) -> pd.DataFrame:
    """Compute ASR with Clopper-Pearson 95% CI for each model × condition."""
    rows = []
    for model, model_data in results.items():
        for cond in CONDITION_ORDER:
            if cond not in model_data:
                continue
            data = model_data[cond]
            judgments = [d["judgment"] for d in data]
            # Exclude errors
            valid = [j for j in judgments if not j.get("error", False)]
            n_harmful = sum(1 for j in valid if j.get("harmful", False))
            n_total = len(valid)
            asr = n_harmful / n_total if n_total > 0 else 0

            # Clopper-Pearson CI
            ci_lo, ci_hi = proportion_confint(n_harmful, n_total, alpha=0.05, method="beta")

            # Mean severity score
            scores = [j.get("score", 0) for j in valid if j.get("score", 0) > 0]
            mean_score = np.mean(scores) if scores else 0

            rows.append({
                "model": model,
                "condition": cond,
                "condition_label": CONDITION_LABELS[cond],
                "n_harmful": n_harmful,
                "n_total": n_total,
                "asr": asr,
                "ci_lo": ci_lo,
                "ci_hi": ci_hi,
                "mean_score": mean_score,
            })
    return pd.DataFrame(rows)


def compute_cohens_h(p1: float, p2: float) -> float:
    """Compute Cohen's h effect size for two proportions."""
    return 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))


def statistical_tests(results: dict, asr_df: pd.DataFrame) -> list[dict]:
    """Run McNemar's test comparing each condition vs direct baseline."""
    test_results = []
    for model in results:
        if "direct" not in results[model]:
            continue
        direct_data = results[model]["direct"]
        direct_judgments = [d["judgment"] for d in direct_data]

        for cond in CONDITION_ORDER[1:]:  # skip direct
            if cond not in results[model]:
                continue
            cond_data = results[model][cond]
            cond_judgments = [d["judgment"] for d in cond_data]

            # Build contingency: paired comparisons (same behavior, different condition)
            n = min(len(direct_judgments), len(cond_judgments))
            # McNemar's: count discordant pairs
            b = 0  # direct=not harmful, cond=harmful
            c = 0  # direct=harmful, cond=not harmful
            for i in range(n):
                dj = direct_judgments[i]
                cj = cond_judgments[i]
                if dj.get("error") or cj.get("error"):
                    continue
                d_harm = dj.get("harmful", False)
                c_harm = cj.get("harmful", False)
                if not d_harm and c_harm:
                    b += 1
                elif d_harm and not c_harm:
                    c += 1

            # McNemar's test (exact binomial for small counts)
            if b + c > 0:
                p_val = stats.binomtest(b, b + c, 0.5).pvalue if (b + c) < 25 else None
                if p_val is None:
                    # Chi-squared approximation
                    chi2 = (abs(b - c) - 1) ** 2 / (b + c)
                    p_val = stats.chi2.sf(chi2, 1)
            else:
                p_val = 1.0

            # Effect size
            row_direct = asr_df[(asr_df["model"] == model) & (asr_df["condition"] == "direct")]
            row_cond = asr_df[(asr_df["model"] == model) & (asr_df["condition"] == cond)]
            if len(row_direct) > 0 and len(row_cond) > 0:
                h = compute_cohens_h(row_cond.iloc[0]["asr"], row_direct.iloc[0]["asr"])
            else:
                h = 0

            test_results.append({
                "model": model,
                "comparison": f"direct vs {cond}",
                "b_discordant": b,
                "c_discordant": c,
                "p_value": p_val,
                "cohens_h": h,
                "significant_bonf": p_val < 0.00625,  # 0.05/8 comparisons
            })

    return test_results


def plot_asr_comparison(asr_df: pd.DataFrame):
    """Bar chart comparing ASR across conditions for each model."""
    models = asr_df["model"].unique()
    n_models = len(models)

    fig, axes = plt.subplots(1, n_models, figsize=(6 * n_models, 5), sharey=True)
    if n_models == 1:
        axes = [axes]

    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

    for ax, model in zip(axes, models):
        df_m = asr_df[asr_df["model"] == model].sort_values(
            "condition", key=lambda x: x.map({c: i for i, c in enumerate(CONDITION_ORDER)})
        )
        x = np.arange(len(df_m))
        bars = ax.bar(x, df_m["asr"], color=colors[:len(df_m)],
                      yerr=[df_m["asr"] - df_m["ci_lo"], df_m["ci_hi"] - df_m["asr"]],
                      capsize=4, edgecolor="black", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(df_m["condition_label"], fontsize=9)
        ax.set_title(model, fontsize=13, fontweight="bold")
        ax.set_ylabel("Attack Success Rate (ASR)" if ax == axes[0] else "")
        ax.set_ylim(0, 1.0)
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.grid(axis="y", alpha=0.3)

        # Add value labels
        for bar, val in zip(bars, df_m["asr"]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=9)

    fig.suptitle("Attack Success Rate by Prompting Condition", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "asr_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {FIGURES_DIR / 'asr_comparison.png'}")


def plot_severity_distribution(results: dict):
    """Box plot of severity scores across conditions."""
    models = list(results.keys())
    n_models = len(models)

    fig, axes = plt.subplots(1, n_models, figsize=(6 * n_models, 5), sharey=True)
    if n_models == 1:
        axes = [axes]

    for ax, model in zip(axes, models):
        data_by_cond = []
        labels = []
        for cond in CONDITION_ORDER:
            if cond not in results[model]:
                continue
            scores = [d["judgment"].get("score", 0) for d in results[model][cond]
                     if not d["judgment"].get("error", False) and d["judgment"].get("score", 0) > 0]
            data_by_cond.append(scores)
            labels.append(CONDITION_LABELS[cond])

        bp = ax.boxplot(data_by_cond, labels=labels, patch_artist=True)
        colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_title(model, fontsize=13, fontweight="bold")
        ax.set_ylabel("Severity Score (1-5)" if ax == axes[0] else "")
        ax.set_ylim(0.5, 5.5)
        ax.grid(axis="y", alpha=0.3)

    fig.suptitle("Response Severity Distribution by Condition", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "severity_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {FIGURES_DIR / 'severity_distribution.png'}")


def plot_asr_heatmap(asr_df: pd.DataFrame):
    """Heatmap of ASR values across models and conditions."""
    pivot = asr_df.pivot(index="model", columns="condition", values="asr")
    pivot = pivot[CONDITION_ORDER]  # order columns

    fig, ax = plt.subplots(figsize=(10, 3 + 0.5 * len(pivot)))
    im = ax.imshow(pivot.values, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=1)

    ax.set_xticks(range(len(CONDITION_ORDER)))
    ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITION_ORDER], fontsize=9)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=10)

    # Annotate cells
    for i in range(len(pivot.index)):
        for j in range(len(CONDITION_ORDER)):
            val = pivot.values[i, j]
            color = "white" if val > 0.5 else "black"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", color=color, fontsize=11)

    plt.colorbar(im, ax=ax, label="ASR")
    ax.set_title("ASR Heatmap: Model × Prompting Condition", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "asr_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {FIGURES_DIR / 'asr_heatmap.png'}")


def run_analysis():
    """Run full analysis pipeline."""
    FIGURES_DIR.mkdir(exist_ok=True)

    results = load_results()
    print(f"Loaded results for models: {list(results.keys())}")

    # Compute ASR table
    asr_df = compute_asr_table(results)
    print("\n" + "=" * 70)
    print("ASR Results (with 95% Clopper-Pearson CI)")
    print("=" * 70)
    for _, row in asr_df.iterrows():
        print(f"  {row['model']:15s} | {row['condition']:30s} | "
              f"ASR={row['asr']:.3f} [{row['ci_lo']:.3f}, {row['ci_hi']:.3f}] "
              f"({row['n_harmful']}/{row['n_total']}) | MeanScore={row['mean_score']:.2f}")

    # Save ASR table
    asr_df.to_csv(RESULTS_DIR / "asr_table.csv", index=False)

    # Statistical tests
    print("\n" + "=" * 70)
    print("Statistical Tests (McNemar's, Bonferroni-corrected)")
    print("=" * 70)
    test_results = statistical_tests(results, asr_df)
    for t in test_results:
        sig = "***" if t["significant_bonf"] else "n.s."
        print(f"  {t['model']:15s} | {t['comparison']:35s} | "
              f"p={t['p_value']:.4f} | h={t['cohens_h']:.3f} | {sig}")

    with open(RESULTS_DIR / "statistical_tests.json", "w") as f:
        json.dump(test_results, f, indent=2, default=str)

    # Over-refusal rates
    print("\n" + "=" * 70)
    print("Over-Refusal Rates (XSTest)")
    print("=" * 70)
    for model in results:
        if "xstest_overrefusal" in results[model]:
            orr = results[model]["xstest_overrefusal"]
            print(f"  {model}: {orr['n_refused']}/{orr['n_total']} = {orr['rate']:.3f}")

    # Generate visualizations
    print("\nGenerating visualizations...")
    plot_asr_comparison(asr_df)
    plot_severity_distribution(results)
    plot_asr_heatmap(asr_df)

    # Summary statistics for report
    summary = {
        "asr_by_model_condition": asr_df.to_dict("records"),
        "statistical_tests": test_results,
        "overrefusal": {m: results[m].get("xstest_overrefusal", {}).get("rate", None) for m in results},
    }
    with open(RESULTS_DIR / "analysis_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nAnalysis summary saved to {RESULTS_DIR / 'analysis_summary.json'}")

    return asr_df, test_results


if __name__ == "__main__":
    asr_df, tests = run_analysis()
