## Groww Mutual Fund RAG Chatbot

A **facts-only** FAQ chatbot for **Groww Mutual Fund** schemes using **Retrieval-Augmented Generation (RAG)**. Built as a learning project for fintech + RAG, aligned with the **Mutual Fund FAQ Assistant – Milestone 1** brief.

Structure and sections are inspired by the HDFC RAG chatbot README in `arvikode/grow_RAG_Based_Mutual_Fund_FAQ_Chatbot`, adapted for Groww.

---

## 📋 Project Overview

- **Assignment**: RAG-based Mutual Fund FAQ Chatbot – Milestone 1  
- **Product**: Groww (Groww Asset Management Limited)  
- **Scope**: Answer **factual questions** about Groww mutual fund schemes using **official public sources only**  
- **Interface**: Streamlit web app (+ CLI helper)

### Key Features

- **Facts-only responses** (no investment advice)  
- **One source citation** in every answer  
- **5 Groww mutual fund schemes** covered  
- **25 official sources** (Groww, GrowwMF, KFintech, MF Central, AMFI, SEBI)  
- **Polite refusal** of advice/portfolio/PII questions  
- Short, clear answers with **“Last updated from sources: …”**

---

## 🎯 Scope

### AMC Selected

- **Groww Mutual Fund** (Groww Asset Management Limited)

### Schemes Covered (5)

1. **Groww Nifty 50 Index Fund** – Large-cap index equity  
2. **Groww Value Fund** – Large-cap equity (Value)  
3. **Groww ELSS Tax Saver Fund** – ELSS / tax-saving equity with 3-year lock-in  
4. **Groww Multicap Fund** – Multi-cap equity  
5. **Groww Liquid Fund** – Debt (Liquid)

### Questions Answered (Factual)

- Expense ratio (Direct / Regular)  
- Exit load and redemption conditions  
- Minimum SIP / lump sum amount  
- Lock-in period (ELSS: 3 years)  
- Riskometer level  
- Benchmark index  
- How to download account / capital gains statements  

### Questions Refused (Advice / PII)

- “Should I invest in this fund?”  
- “Which scheme is better?”  
- “How much should I invest?”  
- Any query involving **PAN, Aadhaar, account numbers, OTP, email, phone**

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                      │
│                 (Streamlit Web App + CLI)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Question Processing                      │
│         (Intent Detection + Advice/PII Guardrails)          │
└────────────────────────┬────────────────────────────────────┘
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
         [Factual Q]        [Advice / PII Q]
                │                 │
                │                 └──► Polite Refusal
                │                      + Educational Link
                ▼
┌─────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Embedding    │→ │ Vector Store │→ │ Retrieval    │      │
│  │ (Query Text) │  │ (ChromaDB)   │  │ (Top-k docs) │      │
│  └──────────────┘  └──────────────┘  └──────┬───────┘      │
└────────────────────────────────────────────┬────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Answer Formatting                         │
│  - Use retrieved chunks directly (no external LLM)          │
│  - Keep answer ≤3 sentences                                 │
│  - Always include source URL                                │
│  - Add “Last updated from sources: [month year]”            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Response Display                         │
│      (Answer + Citation + Timestamp + Disclaimer)           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```text
groww-mf-faq/
├── app.py                        # Streamlit UI (main entry for web)
├── groww_mf_faq_assistant.py    # CLI interface (terminal Q&A)
├── README.md                    # This file
├── DISCLAIMER.md                # Disclaimer + refusal snippets
├── disclaimer.txt               # Short disclaimer text
│
├── corpus/                      # RAG corpus (facts in markdown)
│   ├── 06_riskometer_benchmark.md
│   ├── 10_groww_elss_expense_sip_lockin.md
│   ├── 11_groww_value_exit_risk_benchmark.md
│   ├── 12_groww_liquid_charges.md
│   ├── 13_groww_statements_capital_gains.md
│   ├── 14_groww_nifty50_expense_benchmark.md
│   └── ... (supporting general FAQs)
│
├── src/
│   ├── __init__.py              # Makes src a package
│   ├── config.py                # Paths, model name, constants
│   ├── corpus_loader.py         # Load & chunk corpus with source URLs
│   ├── rag.py                   # Build Chroma index + answer_factual_query
│   └── refusal.py               # Advice/PII detection and refusal messages
│
├── sources/
│   ├── sources.csv              # 25 official URLs (Groww, KFintech, MF Central, AMFI, SEBI)
│   └── SOURCES.md               # Same list in markdown form
│
├── sample_qa.md                 # 10 sample Q&A pairs (Groww-specific)
├── chroma_db/                   # Chroma persistent index (created at runtime)
└── requirements.txt             # Python dependencies
```

---

## 🛠️ Tech Stack

| **Component** | **Technology**                               | **Purpose**                      |
|---------------|----------------------------------------------|----------------------------------|
| Language      | Python 3.10+                                 | Core development                 |
| UI            | Streamlit                                    | Web interface                    |
| CLI           | Python script (`input()` loop)               | Terminal assistant               |
| Embeddings    | `sentence-transformers` (`all-MiniLM-L6-v2`) | Text → dense vectors             |
| Vector DB     | ChromaDB                                     | Store & retrieve embeddings      |
| Data format   | Markdown (`corpus/*.md`)                     | Curated Groww/AMFI/SEBI facts    |

---

## 📊 Data Sources (25 Official URLs)

The assistant uses only **official public sources**:

- **Groww / Groww Mutual Fund**
  - AMC and scheme pages for expense ratio, exit load, minimum SIP  
  - Scheme detail pages for Nifty 50, ELSS, Multicap, Value, Liquid  
  - Groww Help Center (statements, tax documents)  
  - Groww blog on reading mutual fund factsheets  

- **Groww AMC compliance docs**
  - SID – Groww ELSS Tax Saver Fund  
  - KIM – Groww Nifty 50 Index Fund  

- **RTA / Statements**
  - KFintech RTA portal + capital gains statement page  
  - MF Central consolidated statement + knowledge center  

- **AMFI**
  - Riskometer explanation  
  - Investor FAQs  
  - Scheme information, NAV history, knowledge center  

- **SEBI**
  - Investor education corner  
  - Relevant regulations  

Full list with IDs, URLs, and descriptions: see `sources/sources.csv` and `sources/SOURCES.md`.

---

## 🚀 Development Phases

### Phase 1 – Corpus & Sources (Complete)

- Selected **Groww AMC** and 5 schemes  
- Collected **25 official URLs** from Groww, GrowwMF, KFintech, MF Central, AMFI, SEBI  
- Authored corpus markdown files in `corpus/` with:
  - Short factual paragraphs
  - Embedded `Source: URL` for each fact block  
- Created `sources/sources.csv` and `sources/SOURCES.md`  
- Prepared `sample_qa.md` with 10 Groww Q&A examples  

---

### Phase 2 – RAG Pipeline (Complete)

- Implemented corpus loading and chunking in `src/corpus_loader.py`  
- Generated embeddings with `sentence-transformers`  
- Stored document embeddings in **ChromaDB** (persistent index in `chroma_db/`)  
- Implemented `answer_factual_query()` in `src/rag.py` to:
  - Retrieve top-k relevant chunks  
  - Extract a concise answer (≤3 sentences)  
  - Return answer text + citation URL  

---

### Phase 3 – Guardrails (Complete)

- Implemented advice/portfolio detection in `src/refusal.py`  
- Added polite refusal messages:
  - “Facts-only; no ‘should I buy/sell’ answers”  
  - Educational link to Groww/AMFI/SEBI content  
- Ensured **no PII** is accepted or processed  

---

### Phase 4 – UI & CLI (Complete)

- Built **Streamlit UI** (`app.py`):
  - Welcome section + scope description  
  - 7 example question buttons (from `sample_qa.md`)  
  - Chat input for free-form queries  
  - Answer area with text + source URL + last-updated note  
  - Footer disclaimer  
- Added **CLI** (`groww_mf_faq_assistant.py`):
  - Same backend logic  
  - Simple Q&A loop with formatted output and citations  

---

## ⚠️ Constraints & Guardrails

### Must Follow

- **Public sources only** – Groww AMC, KFintech, MF Central, AMFI, SEBI  
- **No PII** – No PAN, Aadhaar, account numbers, OTP, email, phone numbers  
- **No performance claims** – No return calculations, comparisons, or forecasts  
- **Facts-only** – No recommendations, ratings, or portfolio advice  
- **Transparency** – One official **source link** in each answer + last-updated note  

### Refusal Criteria

The chatbot **refuses**:

- Investment/portfolio advice (“Should I invest?”, “Which is better?”, “How much should I put?”)  
- Personalized planning or allocation questions  
- Future return predictions  
- Any PII-containing request  

Refusal responses include:

- A clear explanation that only facts are provided  
- A helpful **educational link** (Groww blog / AMFI / SEBI)  
- Examples of factual queries it can answer  

---

## 📝 Sample Interactions

### Factual Question (Answer)

**User:**  
“What is the expense ratio of Groww ELSS Tax Saver Fund?”

**Chatbot (example):**

> Expense Ratio – Groww ELSS Tax Saver Fund  
> Direct Plan: 0.94% per annum  
> Regular Plan: 2.3%  
>  
> Source: `https://groww.in/mutual-funds/amc/groww-mutual-funds`  
> Last updated from sources: February 2026.

---

### Advice Question (Refusal)

**User:**  
“Should I invest in Groww ELSS or Groww Multicap?”

**Chatbot (example):**

> I can only provide factual information about Groww Mutual Fund schemes.  
> I cannot provide investment advice such as “should I buy/sell” or portfolio recommendations.  
> For understanding mutual fund factsheets and key information, please refer to the link below.  
>  
> Learn more: `https://groww.in/blog/mutual-fund-factsheet-key-information-it-holds-and-how-to-read-it`

---

## ✅ Success Criteria (Milestone 1)

- Answers 10+ factual Groww MF questions accurately (`sample_qa.md`)  
- Every answer contains exactly **one official source link**  
- Refuses advice-style questions politely with educational links  
- Answers are **≤3 sentences** (plus citation and timestamp)  
- Uses only **official sources** (Groww, GrowwMF, KFintech, MF Central, AMFI, SEBI)  
- No PII collected or stored  
- Working prototype via **Streamlit** and **CLI**  

---

## 🔧 Setup & Run

### Prerequisites

- Python 3.10+  
- `pip`  
- Internet connection for first-time model download  

### Installation

```bash
git clone <your-repo-url>
cd groww-mf-faq

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

### Run the Web App (Streamlit)

```bash
cd groww-mf-faq
streamlit run app.py
```

Open the URL shown (e.g. `http://localhost:8501`).

### Run the CLI Assistant

```bash
cd groww-mf-faq
python groww_mf_faq_assistant.py
```

> After changing any files in `corpus/`, delete the `chroma_db/` folder and run again to rebuild the index.

---

## ⚠️ Known Limitations

- **Static corpus** – Data is as of **February 2026**; always verify current details on the official source.  
- **No live NAV/performance** – The bot does not fetch real-time data.  
- **English only** – Queries and answers are handled in English.  
- Guardrails are **keyword-based**; some edge cases may need manual refinement.  

---

## 📚 Learning Resources

- Groww blog – Mutual fund factsheet key information  
- AMFI Knowledge Center – Mutual fund basics and riskometer  
- SEBI Investor Education – Regulatory and investor protection content  

(See `sources/sources.csv` for exact URLs used.)

---

## 📄 License & Disclaimer

This project is an **educational demonstration** for the Mutual Fund FAQ Milestone 1.  
It is **not** affiliated with, endorsed by, or reviewed by **Groww Asset Management Limited**.

- Does **not** provide investment advice  
- Past performance does **not** guarantee future results  
- Mutual fund investments are subject to market risks  
- Always read the scheme information documents (SID / KIM) carefully and consult a SEBI-registered advisor for investment decisions  
