from __future__ import annotations
import streamlit as st
import pandas as pd
from pathlib import Path
from utils import get_data_path, configure_logging
from retriever import TfidfFaqRetriever

configure_logging()

st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬", layout="centered")

st.title("💬 Customer Support Chatbot")
st.write("Ask a question about products, billing, contracts, roaming, or support.")

# Sidebar: konfig
st.sidebar.header("Settings")
threshold = st.sidebar.slider("Confidence threshold", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
top_k = st.sidebar.slider("Top-K matches", min_value=1, max_value=5, value=3, step=1)

data_path = get_data_path() / "faq.csv"

def load_faq(path):
    import itertools
    import pandas as pd

    # mulige skilletegn og encodings (Excel/Windows-friendly)
    seps = [",", ";", "\t", "|"]
    encs = ["utf-8-sig", "utf-8", "latin-1"]

    last_err = None
    for sep, enc in itertools.product(seps, encs):
        try:
            df = pd.read_csv(path, sep=sep, encoding=enc, engine="python", on_bad_lines="skip")

            # dropp tomme/unnamed kolonner
            drop_these = [c for c in df.columns if str(c).startswith("Unnamed")]
            if drop_these:
                df = df.drop(columns=drop_these)

            # normaliser kolonnenavn (trim + lower + fjern BOM)
            df.columns = (
                df.columns
                .str.replace("\ufeff", "", regex=False)
                .str.strip()
                .str.lower()
            )

            # map alias -> standard
            alias_map = {
                "category": "category",
                "kategori": "category",
                "cat": "category",

                "question": "question",
                "sporsmal": "question",   # hvis æøå røk i encoding
                "spørsmål": "question",
                "qs": "question",

                "answer": "answer",
                "svar": "answer",
                "ans": "answer",
                "response": "answer",
            }
            df = df.rename(columns={c: alias_map.get(c, c) for c in df.columns})

            # noen ganger har Excel/semicolon ekstra blankkolonner på slutten
            # behold bare de vi trenger hvis de finnes
            needed = {"category", "question", "answer"}
            if needed.issubset(set(df.columns)):
                df = df[list(needed)]
                # trim whitespace i celler
                for col in ["category", "question", "answer"]:
                    df[col] = df[col].astype(str).str.replace("\ufeff", "", regex=False).str.strip()
                # fjern helt tomme rader
                df = df.dropna(how="all")
                # valider at vi faktisk har innhold
                if len(df) == 0:
                    last_err = ValueError("faq.csv ser tom ut etter rensing.")
                    continue
                return df

            # hvis vi ikke har de rette kolonnene, prøv neste kombinasjon
            last_err = ValueError(f"Fant kolonner {list(df.columns)}, mangler 'category, question, answer'")
        except Exception as e:
            last_err = e
            continue

    # hvis ingen kombinasjon funket, kast siste feilmelding
    raise ValueError(f"Kunne ikke lese faq.csv. Siste feil: {last_err}")


# Last FAQ
if not data_path.exists():
    st.error(f"Couldn't find data file at: {data_path}. Add data/faq.csv and reload.")
    st.stop()

faqs = load_faq(data_path)

with st.expander("Debug: file preview"):
    st.write(f"Loaded from: {data_path}")
    st.write(faqs.head())
    st.write({"columns": list(faqs.columns), "rows": len(faqs)})

required_cols = {"category", "question", "answer"}
if not required_cols.issubset(set(faqs.columns)):
    st.error(f"faq.csv must include columns: {required_cols}")
    st.stop()

retriever = TfidfFaqRetriever(faqs)

# UI
user_q = st.text_input("Your question", placeholder="How can I cancel my contract?")
ask = st.button("Ask")

if ask and user_q.strip():
    results = retriever.search(user_q, top_k=top_k)
    best = results[0] if results else None

    if best and best.score >= threshold:
        st.success(best.answer)
        with st.expander("Why this answer? (similar questions)"):
            for r in results:
                st.write(f"- **{r.question}**  (score: {r.score:.3f}, cat: {r.category})")
    else:
        st.warning("Sorry, I’m not confident about the answer. Try rephrasing or pick a related topic below.")

# Forslagseksjon (auto-liste av unike spørsmål)
st.markdown("---")
st.subheader("Popular questions")
for q in faqs["question"].head(8).tolist():
    if st.button(q):
        # Simuler klikk-spørsmål ved å kjøre søk og rendrere svar under knappen
        res = retriever.search(q, top_k=top_k)[0]
        st.info(res.answer)
