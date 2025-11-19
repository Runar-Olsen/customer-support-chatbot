# 💬 Customer Support Chatbot (Python + Streamlit)

En enkel, produksjonsvennlig **FAQ-chatbot** som matcher brukerens spørsmål mot en kunnskapsbase ved hjelp av **TF-IDF + cosine similarity** og viser beste svar i et pent **Streamlit-grensesnitt**.

---

## 🎯 Hva prosjektet demonstrerer
- Databehandling fra en egen FAQ-base (`CSV`)
- Natural Language Retrieval med TF-IDF (ngrams + cosine similarity)
- Dynamisk terskel for tillit til svar + visning av lignende spørsmål
- Streamlit-webapp med interaktivt sidepanel (threshold og top-k)
- Lett å oppgradere til embeddings eller RAG-løsninger

---

## 🗂️ Prosjektstruktur
```text
customer-support-chatbot/
├─ data/
│  └─ faq.csv
│
├─ src/
│  ├─ utils.py
│  ├─ retriever.py
│  └─ app.py
│
├─ .gitignore
├─ requirements.txt
└─ README.md

## ▶️ Kom i gang

1️⃣ Opprett og aktiver virtuelt miljø

python -m venv .venv
 Windows PowerShell:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

2️⃣ Kjør applikasjonen

streamlit run src/app.py

3️⃣ Åpne nettleseren
Streamlit starter automatisk på:
👉 http://localhost:8501

## 🧾 Dataformat

data/faq.csv må inneholde tre kolonner:

category	question	answer
Contract	How can I cancel my contract?	You can cancel via the self-service portal under “My subscription” → “Cancel”, or call support at 21 00 00.
Billing	Why is my invoice higher this month?	Extra charges may include add-ons, roaming, or late fees. Check your invoice details in the portal → “Billing”.
Coverage	Do you have 5G in my area?	Check the coverage map on our website. 5G is available in major cities and expanding monthly.

## 💡 Tips:

Filen må lagres som UTF-8 (Comma delimited) CSV

Har du spørsmål eller svar med komma → bruk anførselstegn rundt teksten

Kolonnenavn må være nøyaktig category, question, answer

## 🧠 Hvordan det fungerer

1️⃣ Bruker skriver et spørsmål i tekstboksen
2️⃣ Modellen konverterer spørsmålet til TF-IDF-vektor
3️⃣ Cosine-similarity måles mot alle spørsmål i FAQ
4️⃣ Topp-k mest like spørsmål hentes og rangeres
5️⃣ Hvis høyeste score > terskel → vis svar
6️⃣ Hvis score < terskel → appen viser “I’m not confident” og lignende spørsmål

## 🧩 Teknologier brukt
- Python
- Streamlit
- Pandas
- Scikit-learn (TfidfVectorizer, cosine_similarity)
- Joblib / utils for logging og stier

## 🧪 Eksempel på bruk

Input:
“Can I use my plan in Europe?”

Output:
“Within EEA you use your domestic allowance at no extra cost. Fair usage limits may apply.”

## 🚀 Videre arbeid (forslag til oppgraderinger)
-💡 Embeddings:
Bytt ut TF-IDF med sentence-transformers for mer presis semantisk matching
-🤖 LLM-fallback:
Koble til OpenAI API / LangChain for “RAG”-modus – hvis modellen er usikker, spør en LLM
-🌐 Flere domener:
Bruk samme rammeverk for intern FAQ, produktkunnskap, HR, IT-support, etc.
-📊 Analyse:
Logg brukerforespørsler og bygg et Power BI-dashboard for innsikt i spørsmålstyper

## 🧭 Forfatter
Runar Olsen
Data Analyst – Python | Power BI | Machine Learning