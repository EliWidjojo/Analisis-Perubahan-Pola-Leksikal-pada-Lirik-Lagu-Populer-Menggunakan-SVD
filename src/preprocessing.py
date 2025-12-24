import re

# 1. Tokenisasi & 2. Normalisasi
def tokenize(text):
    text = text.lower()
    text = re.sub(r"[']", "", text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = text.split()

    return tokens

# 3. Stemming/Lematisasi 
def simple_stem(word):
    suffixes = [
        "ization", "isation",
        "ational", "fulness", "ousness",
        "iveness", "ational", "tional",
        "lessly", "lessly", "lessly",
        "lessly", "ologist", "ologies",
        "lessly", "lessly",
        "ically", "ically",
        "ing", "ers", "ies", "ied",  
        "ness", "ment", "able", "ible",
        "less", "tion", "sion", "ment",
        "ally", "edly", "ward", "wards",
        "est", "ous", "ive", "ish",
        "ed", "ly", "er", "es", "s"
    ]

    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

# 4. Penghapusan Stopword
STOPWORDS = { # set kata2 yang umum
    "a","an","the","is","are","and","or","to","in","of",
    "that","it","on","for","with","as","by","this","was",
    "be","from","at","which","but","not","have","has",
    "had","were","will","their","its",
    "oh", "na", "la", "yeah"
}

def remove_stopwords(tokens): 
    return [t for t in tokens if t not in STOPWORDS]

# Process document
def process_document(text, use_stem=False):
    tokens = tokenize(text)

    if use_stem:
        tokens = [simple_stem(t) for t in tokens]

    tokens = remove_stopwords(tokens)

    return tokens

