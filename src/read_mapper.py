import os
import pandas as pd

def load_texts(min_chars=30):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    metadata_path = os.path.join(BASE_DIR, "../data/metadata.xlsx")
    lyrics_dir    = os.path.join(BASE_DIR, "../data/lyrics")

    df = pd.read_excel(metadata_path)

    texts = []
    labels = []

    for _, row in df.iterrows():
        year = int(row["Year"])
        rank = int(row["Rank"])
        file_id = f"{year}_{rank:03d}.txt"

        txt_path = os.path.join(lyrics_dir, str(year), file_id)

        if not os.path.exists(txt_path):
            continue

        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()

        if len(content) < min_chars:
            continue

        texts.append(content)
        labels.append({
            "year": year,
            "rank": rank,
            "file": file_id
        })

    return texts, labels
