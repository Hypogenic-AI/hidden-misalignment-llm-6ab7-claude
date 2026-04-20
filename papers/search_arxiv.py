"""
Search arXiv for papers related to:
"Probing Hidden Misalignment in Robust LLMs via Adversarial Chain-of-Thought Prompting"

Runs 7 topic searches, deduplicates by arxiv ID, and saves results to
papers/arxiv_results.json.
"""

import json
import time
from pathlib import Path

import arxiv

OUTPUT_PATH = Path(__file__).parent / "arxiv_results.json"
MAX_RESULTS_PER_QUERY = 15

# ------------------------------------------------------------------
# Search queries covering the hypothesis space
# ------------------------------------------------------------------
QUERIES = [
    # 1. LLM misalignment / language model alignment
    'ti:("LLM misalignment") OR ti:("language model alignment") OR '
    'abs:("LLM misalignment" OR "language model alignment")',

    # 2. Adversarial prompting / jailbreak + LLM
    'ti:(jailbreak OR "adversarial prompting") OR '
    'abs:(jailbreak AND ("large language model" OR LLM))',

    # 3. Chain of thought + adversarial or safety
    'ti:("chain of thought") OR '
    'abs:("chain of thought" AND (adversarial OR safety OR alignment))',

    # 4. Alignment robustness / robust alignment
    'ti:("alignment robustness" OR "robust alignment") OR '
    'abs:("alignment robustness" OR "robust alignment")',

    # 5. Sleeper agent / hidden misalignment / deceptive alignment
    'ti:("sleeper agent" OR "hidden misalignment" OR "deceptive alignment") OR '
    'abs:("sleeper agent" OR "hidden misalignment" OR "deceptive alignment")',

    # 6. Red teaming + language model
    'ti:("red teaming" OR "red-teaming") OR '
    'abs:("red teaming" AND ("language model" OR LLM))',

    # 7. Safety evaluation + language model
    'ti:("safety evaluation") OR '
    'abs:("safety evaluation" AND ("language model" OR LLM))',
]


def fetch_results(query: str, max_results: int = MAX_RESULTS_PER_QUERY) -> list[dict]:
    """Run one arXiv search query and return a list of paper dicts."""
    client = arxiv.Client(
        page_size=max_results,
        delay_seconds=3.0,   # be polite to the API
        num_retries=3,
    )
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers = []
    for result in client.results(search):
        arxiv_id = result.entry_id.split("/")[-1]   # e.g. "2401.12345v1" → strip to ID
        # Normalise: strip version suffix for dedup key
        base_id = arxiv_id.split("v")[0]

        papers.append({
            "arxiv_id": base_id,
            "title": result.title.strip(),
            "authors": [a.name for a in result.authors],
            "abstract": result.summary.strip(),
            "published": result.published.strftime("%Y-%m-%d") if result.published else "",
            "pdf_url": result.pdf_url or "",
            "categories": result.categories,
        })
    return papers


def main():
    all_papers: dict[str, dict] = {}   # keyed by base arxiv_id for dedup

    for idx, query in enumerate(QUERIES, start=1):
        print(f"\n[{idx}/{len(QUERIES)}] Query: {query[:80]}...")
        try:
            results = fetch_results(query)
            new_count = 0
            for paper in results:
                aid = paper["arxiv_id"]
                if aid not in all_papers:
                    all_papers[aid] = paper
                    new_count += 1
            print(f"  -> {len(results)} returned, {new_count} new (total so far: {len(all_papers)})")
        except Exception as exc:
            print(f"  !! Error on query {idx}: {exc}")
        # small extra sleep between queries to avoid rate limits
        time.sleep(2)

    # Convert to sorted list (by published date descending, then title)
    paper_list = sorted(
        all_papers.values(),
        key=lambda p: (p["published"], p["title"]),
        reverse=True,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(paper_list, fh, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(paper_list)} unique papers saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
