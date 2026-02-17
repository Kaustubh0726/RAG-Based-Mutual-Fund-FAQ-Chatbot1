# Groww Mutual Fund FAQ Chatbot – Streamlit UI
# Facts-only. No investment advice. One citation per answer.

import streamlit as st
from src.rag import answer_factual_query, get_app_store
from src.refusal import is_advice_or_opinion_query, get_refusal_response

st.set_page_config(
    page_title="Groww Mutual Fund FAQ",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Disclaimer snippet (used in UI)
DISCLAIMER = "Facts-only. No investment advice."

# Welcome and scope
st.markdown("## Groww Mutual Fund FAQ")
st.markdown("Ask factual questions about mutual fund schemes (e.g. expense ratio, exit load, minimum SIP, ELSS lock-in, riskometer, benchmark, statements).")
st.caption(DISCLAIMER)

# Example questions (7, taken from sample_qa.md)
st.markdown("**Example questions:**")
ex1 = "What is the expense ratio of Groww ELSS Tax Saver Fund?"
ex2 = "What is the lock-in period for ELSS fund?"
ex3 = "What is the minimum SIP amount?"
ex4 = "What is the exit load for Groww Value Fund?"
ex5 = "What is the riskometer rating of Groww Nifty 50 Index Fund?"
ex6 = "What is the benchmark of Groww Multicap Fund?"
ex7 = "How to download capital gains statement?"

for ex in [ex1, ex2, ex3, ex4, ex5, ex6, ex7]:
    if st.button(ex, use_container_width=True):
        st.session_state["question"] = ex

# Input
question = st.chat_input("Type your question here...")
if "question" in st.session_state:
    question = st.session_state.get("question")
    del st.session_state["question"]

if question:
    question = question.strip()
    if not question:
        st.stop()

    # Check for advice/opinion → refuse
    if is_advice_or_opinion_query(question):
        msg, link = get_refusal_response(question)
        st.info(msg)
        st.markdown(f"📚 **Learn more:** [Mutual fund factsheet – key information and how to read it]({link})")
        st.markdown("💡 *I can help with factual questions like: expense ratios, exit loads, minimum SIP, lock-in (ELSS), riskometer, benchmark, statements.*")
        st.caption(DISCLAIMER)
        st.stop()

    # Factual: RAG answer + one citation
    with st.spinner("Searching FAQ..."):
        try:
            coll, mod = get_app_store()
            answer, source_url = answer_factual_query(question, collection=coll, model=mod)
        except Exception as e:
            st.error("Something went wrong. Please try again or rephrase.")
            st.caption(str(e))
            st.stop()

    st.markdown(answer)
    st.markdown(f"**Source:** [Official link]({source_url})")
    st.caption(DISCLAIMER)

st.markdown("---")
st.caption("Last updated from sources: February 2026. Scope: Groww Mutual Fund schemes; AMC/KFintech/MF Central public pages. No PII collected.")
