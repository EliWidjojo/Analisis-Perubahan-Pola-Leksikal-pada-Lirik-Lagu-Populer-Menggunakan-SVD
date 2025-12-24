import numpy as np
from preprocessing import process_document

def tf_idf(texts, use_stem=True):
    docs_tokens = [
        process_document(t, use_stem=use_stem)
        for t in texts
    ]

    vocab = sorted(set(token for doc in docs_tokens for token in doc))
    vocab_index = {w: i for i, w in enumerate(vocab)}
    num_terms = len(vocab)
    num_docs = len(docs_tokens)
    A = np.zeros((num_terms, num_docs), dtype=float)

    for j, tokens in enumerate(docs_tokens):
        for token in tokens:
            A[vocab_index[token], j] += 1

    col_sums = A.sum(axis=0)
    valid = col_sums > 0
    A = A[:, valid]
    col_sums = col_sums[valid]
    num_docs = A.shape[1]
    tf = A / col_sums
    df = np.count_nonzero(A > 0, axis=1)
    idf = np.log10(num_docs / (1 + df))
    X = tf * idf[:, np.newaxis]

    return X, valid
