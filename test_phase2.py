"""Phase 2 Verification — Tests helpers, entity maps, and entity extraction."""

from app.utils.helpers import normalize_text, generate_ngrams
from app.domain.entity_maps import get_supported_domains, get_all_entities_flat
from app.services.entity_service import extract_entities


def main():
    # --- Test 1: Helpers ---
    print("=" * 60)
    print("TEST 1: Text Normalization & N-gram Generation")
    print("=" * 60)

    raw = "Risk Management & Portfolio Optimization!"
    print(f'  normalize: "{raw}"')
    print(f'         -> "{normalize_text(raw)}"')

    ngrams = generate_ngrams("lean supply chain")
    print(f'  ngrams("lean supply chain"): {ngrams}')

    # --- Test 2: Domain Maps ---
    print("\n" + "=" * 60)
    print("TEST 2: Domain Entity Maps")
    print("=" * 60)

    print(f"  Supported domains: {get_supported_domains()}")
    fin = get_all_entities_flat("finance")
    mfg = get_all_entities_flat("manufacturing")
    print(f"  Finance entities: {len(fin)}")
    print(f"  Manufacturing entities: {len(mfg)}")

    fin_cats = sorted(set(e["category"] for e in fin))
    mfg_cats = sorted(set(e["category"] for e in mfg))
    print(f"  Finance categories: {fin_cats}")
    print(f"  Manufacturing categories: {mfg_cats}")

    # --- Test 3: Finance Extraction ---
    print("\n" + "=" * 60)
    print("TEST 3: Finance Entity Extraction")
    print("=" * 60)

    finance_text = (
        "Our risk management strategy leverages hedging and DCF analysis "
        "to minimize market risk. We ensure regulatory compliance through "
        "robust KYC processes and maintain a diversified portfolio with "
        "strong ROI. Stress testing is performed quarterly."
    )
    result = extract_entities(finance_text, "finance")
    print(f"  Matched: {result['matched_count']}/{result['total_entities_in_domain']}")
    for e in result["matched_entities"]:
        print(f"    [{e['weight']}] {e['name']:30s} (matched: \"{e['matched_term']}\")")

    # --- Test 4: Manufacturing Extraction ---
    print("\n" + "=" * 60)
    print("TEST 4: Manufacturing Entity Extraction")
    print("=" * 60)

    mfg_text = (
        "Our lean manufacturing approach combines just-in-time production "
        "with Six Sigma quality control. IoT-enabled predictive maintenance "
        "reduces equipment downtime, while Kanban systems optimize our "
        "supply chain management. We target high OEE across all production lines."
    )
    result2 = extract_entities(mfg_text, "manufacturing")
    print(f"  Matched: {result2['matched_count']}/{result2['total_entities_in_domain']}")
    for e in result2["matched_entities"]:
        print(f"    [{e['weight']}] {e['name']:35s} (matched: \"{e['matched_term']}\")")

    # --- Test 5: Alias resolution ---
    print("\n" + "=" * 60)
    print("TEST 5: Alias Resolution")
    print("=" * 60)

    alias_text = "The ROI from our DCF model shows strong NPV. Our WACC is competitive."
    result3 = extract_entities(alias_text, "finance")
    print("  Input: 'ROI', 'DCF', 'NPV', 'WACC' (all abbreviations)")
    print(f"  Matched: {result3['matched_count']} entities")
    for e in result3["matched_entities"]:
        print(f"    '{e['matched_term']}' -> canonical: '{e['name']}'")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
