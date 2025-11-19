# src/retriever.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Retrieved:
    score: float
    question: str
    answer: str
    category: str
    idx: int


class TfidfFaqRetriever:
    def __init__(self, faqs: pd.DataFrame):
        """
        faqs: DataFrame med kolonner ['category','question','answer']
        """
        self.faqs = faqs.reset_index(drop=True)
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),            # unigram + bigram for bedre matching
            min_df=1,
            stop_words="english",          # ok for engelske spørsmål
        )
        self.matrix = self.vectorizer.fit_transform(self.faqs["question"].values)

    def search(self, query: str, top_k: int = 3) -> List[Retrieved]:
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix).ravel()
        top_idx = sims.argsort()[::-1][:top_k]
        results: List[Retrieved] = []
        for i in top_idx:
            results.append(
                Retrieved(
                    score=float(sims[i]),
                    question=self.faqs.loc[i, "question"],
                    answer=self.faqs.loc[i, "answer"],
                    category=self.faqs.loc[i, "category"],
                    idx=int(i),
                )
            )
        return results
