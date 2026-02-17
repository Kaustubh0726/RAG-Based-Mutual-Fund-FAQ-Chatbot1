# Groww Mutual Fund FAQ Assistant

**Milestone 1: Facts-Only Q&A System**

A RAG-based FAQ assistant that answers factual questions about Groww Mutual Fund schemes using only official public sources. Every answer includes one source link. It does not give investment advice.

**Product:** Groww (Groww Asset Management Limited)

---

## Quick start

### Option 1: Web interface (recommended)

```bash
# From project root (groww-mf-faq)
pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown (e.g. http://localhost:8501).

### Option 2: Command line

```bash
pip install -r requirements.txt
python groww_mf_faq_assistant.py
```

First run may download the embedding model (~90 MB). The vector index is built automatically on first use.

---

## Scope

| Item | Details |
|------|---------|
| **AMC** | Groww Asset Management Limited |
| **Schemes** | 5 schemes (see below) |
| **Corpus** | 15–25 public pages from AMC, SEBI, AMFI, KFintech, MF Central |

**Schemes covered**

1. Groww Nifty 50 Index Fund (Large Cap Index)  
2. Groww Value Fund (Large Cap Equity – Value)  
3. Groww ELSS Tax Saver Fund (ELSS / Tax Saver)  
4. Groww Multicap Fund (Multi Cap Equity)  
5. Groww Liquid Fund (Debt – Liquid)

---

## What the assistant does

**Answers factual questions about:**

- Expense ratios (Direct & Regular plan)
- Exit loads and redemption conditions
- Minimum SIP and lumpsum (Rs. 500)
- Lock-in period (ELSS: 3 years)
- Riskometer ratings
- Benchmark indices
- How to download capital gains / account statements

**Does not provide:**

- Investment advice (“Should I buy/sell?”)
- Performance predictions or return comparisons
- Portfolio recommendations

---

## Files in this package

| File | Purpose |
|------|---------|
| `app.py` | Streamlit web UI |
| `groww_mf_faq_assistant.py` | CLI interface |
| `README.md` | This file – setup, scope, limits |
| `sample_qa.md` | 10 example Q&A pairs with answers and links |
| `sources/sources.csv` | 25 official source URLs |
| `sources/SOURCES.md` | Source list (markdown) |
| `DISCLAIMER.md` | Legal disclaimer and UI snippets |
| `disclaimer.txt` | Short disclaimer text for UI |
| `corpus/` | Markdown documents used for RAG retrieval |
| `src/` | RAG, refusal logic, config, corpus loader |

---

## Example questions

- What is the expense ratio of Groww ELSS Tax Saver Fund?
- What is the exit load for Groww Value Fund?
- What is the minimum SIP amount?
- What is the lock-in period for ELSS?
- What is the riskometer rating of Groww Nifty 50 Index Fund?
- What is the benchmark of Groww Multicap Fund?
- How to download capital gains statement?

---

## Data sources

All answers are based on:

- Groww AMC official website (groww.in, growwmf.in)
- Official SIDs and KIMs (Scheme Information Documents, Key Information Memorandums)
- KFintech RTA (mfs.kfintech.com)
- MF Central (mfcentral.com)
- AMFI and SEBI investor education pages

See `sources/sources.csv` for the full list of 25 URLs.

---

## Features

- **RAG retrieval:** Small corpus (markdown chunks) with sentence-transformers embeddings and ChromaDB; one citation per answer.
- **Refusal handling:** Polite “facts-only” refusal for advice/recommendation questions, with an educational link.
- **Web UI:** Welcome line, three example question buttons, chat-style input, “Facts-only. No investment advice.” note.
- **CLI:** Same backend; question prompt and formatted answer with source link.

---

## Privacy and compliance

- **No PII:** Does not accept or store PAN, Aadhaar, account numbers, OTPs, emails, or phone numbers.
- **Public sources only:** AMC / SEBI / AMFI official documents and pages; no third-party blogs as sources.
- **No performance claims:** Does not compute or compare returns; may link to official factsheet when relevant.
- **Disclaimer:** Shown in UI and in `DISCLAIMER.md` / `disclaimer.txt`.

---

## Documentation

| Document | Use |
|----------|-----|
| `README.md` | Setup, scope, and known limits |
| `sample_qa.md` | 10 tested Q&A examples |
| `sources/sources.csv` | All 25 source URLs |
| `DISCLAIMER.md` | Full disclaimer and refusal text |
| `disclaimer.txt` | Short disclaimer for UI |

---

## Quick test

**CLI:**

```bash
python groww_mf_faq_assistant.py
```

At the prompt, try:

```
Your Question: What is the expense ratio of Groww ELSS fund?
```

You should see an answer with Direct/Regular expense ratio and a source link.

**Web:** Run `streamlit run app.py`, click an example question or type the same query.

---

## Known limits

- Corpus is **static** (markdown files). Live websites are not scraped at runtime; data is as of February 2026.
- Confirm current figures (expense ratio, exit load, etc.) on the linked official source.
- Refusal is keyword/heuristic-based; some advice-like phrasings may not be detected.
- English only.

**After changing corpus:** Delete the `chroma_db` folder and run the app again to rebuild the vector index.

---

## Disclaimer

This is a facts-only information assistant. It does not provide investment advice. Information is from public sources as of February 2026. Past performance does not guarantee future results. Mutual fund investments are subject to market risks. Consult a SEBI-registered advisor for investment decisions.

**Groww Mutual Fund contact:**  
Email: iro@growwmf.in | Website: https://growwmf.in/

---

## Milestone 1 requirements

- [x] Working prototype (Streamlit + CLI)
- [x] Source list: 25 official URLs (sources.csv)
- [x] README with setup, scope, and known limits
- [x] Sample Q&A: 10 queries with answers and links (sample_qa.md)
- [x] Disclaimer snippet in UI and in disclaimer.txt / DISCLAIMER.md
- [x] One AMC (Groww), 3–5 schemes (5 schemes)
- [x] Facts-only answers with one citation per answer
- [x] No PII collection

---

## Skills demonstrated

- **W1 – Thinking like a model:** Identify the fact asked; decide answer vs. refuse.
- **W2 – LLMs & prompting:** Concise answers, polite refusals, clear citation wording.
- **W3 – RAG:** Small-corpus retrieval with citations from AMC/SEBI/AMFI-style content.

---

**Version:** 1.0  
**Date:** February 2026  
**Milestone:** 1 – Mutual Fund FAQs (Facts-Only Q&A)

*Educational demonstration. Not affiliated with or endorsed by Groww Asset Management Limited.*
