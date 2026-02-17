#!/usr/bin/env python3
"""
Groww Mutual Fund FAQ Assistant – CLI
Facts-only Q&A using RAG. No investment advice.
Run from project root: python groww_mf_faq_assistant.py
"""

import sys
from pathlib import Path

# Ensure project root is on path so "src" package is found
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag import answer_factual_query, get_app_store
from src.refusal import is_advice_or_opinion_query, get_refusal_response

DISCLAIMER = "Facts-only. No investment advice."


def main():
    print("=" * 60)
    print("Groww Mutual Fund FAQ Assistant")
    print("=" * 60)
    print("\nFacts-only Q&A. No investment advice.\n")
    print("Schemes covered:")
    print("  1. Groww Nifty 50 Index Fund")
    print("  2. Groww Value Fund")
    print("  3. Groww ELSS Tax Saver Fund")
    print("  4. Groww Multicap Fund")
    print("  5. Groww Liquid Fund")
    print("\n" + "=" * 60)
    print("\nExample questions:")
    print("  • What is the expense ratio of Groww ELSS fund?")
    print("  • What is the exit load for Value Fund?")
    print("  • What is the minimum SIP amount?")
    print("  • What is the lock-in period for ELSS?")
    print("  • What is the riskometer rating of Nifty 50 fund?")
    print("  • What is the benchmark of Multicap Fund?")
    print("  • How to download capital gains statement?")
    print("\n" + "=" * 60)
    print(f"\nNote: {DISCLAIMER}")
    print("\nType 'exit' or 'quit' to quit.\n")

    while True:
        try:
            query = input("Your Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not query:
            print("Please enter a question.\n")
            continue

        if query.lower() in ("exit", "quit", "bye"):
            print("\nThank you for using Groww MF FAQ Assistant.")
            break

        print("\n" + "-" * 60)

        if is_advice_or_opinion_query(query):
            msg, link = get_refusal_response(query)
            print(msg)
            print(f"\nLearn more: {link}")
            print("\nI can help with: expense ratios, exit loads, minimum SIP,")
            print("lock-in (ELSS), riskometer, benchmark, statements.")
        else:
            try:
                coll, model = get_app_store()
                answer, source_url = answer_factual_query(query, collection=coll, model=model)
                print(answer)
                print(f"\nSource: {source_url}")
            except Exception as e:
                print("Something went wrong. Please try again or rephrase.")
                print(f"(Error: {e})")

        print("-" * 60)
        print(f"\n{DISCLAIMER}\n")


if __name__ == "__main__":
    main()
