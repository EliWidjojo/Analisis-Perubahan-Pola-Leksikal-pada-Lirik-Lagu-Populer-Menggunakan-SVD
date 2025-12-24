import lyricsgenius
import pandas as pd
import os
import re
import time

# Cleaning
def clean_title(title: str) -> str:
    title = title.split('/')[0]

    title = title.replace('"', '').strip()

    title = re.sub(r'\s+', ' ', title)

    return title.strip()


def clean_artist(artist: str) -> str:
    artist = artist.replace('"', '').strip()
    artist = re.sub(
        r'(featuring|feat\.|with|and|&).*',
        '',
        artist,
        flags=re.I
    )
    artist = re.sub(r'\s+', ' ', artist)
    return artist.strip()

def clean_lyrics(text: str) -> str:
    text = re.sub(r'You might also like.*', '', text, flags=re.DOTALL)
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

# Configuration
GENIUS_TOKEN = ""
METADATA_FILE = "../data/metadata.xlsx"
OUTPUT_DIR = "../data/lyrics"
SLEEP_TIME = 1.0

# Genius Client
genius = lyricsgenius.Genius(
    GENIUS_TOKEN,
    remove_section_headers=True,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    timeout=15
)

# Load Metadata
if METADATA_FILE.endswith(".xlsx"):
    df = pd.read_excel(METADATA_FILE)
else:
    df = pd.read_csv(METADATA_FILE)

os.makedirs(OUTPUT_DIR, exist_ok=True)

failed = []

# Download lyrics
for _, row in df.iterrows():
    year = int(row["Year"])
    rank = int(row["Rank"])
    raw_title = str(row["Title"])
    raw_artist = str(row["Artist"])

    title = clean_title(raw_title)
    artist = clean_artist(raw_artist)

    file_id = f"{year}_{rank:03d}"

    year_dir = os.path.join(OUTPUT_DIR, str(year))
    os.makedirs(year_dir, exist_ok=True)

    out_path = os.path.join(year_dir, f"{file_id}.txt")

    if os.path.exists(out_path):
        continue

    try:
        song = genius.search_song(title, artist)
        if song and song.lyrics:
            lyrics = clean_lyrics(song.lyrics)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(lyrics)
        else:
            failed.append(file_id)

    except Exception:
        failed.append(file_id)

    time.sleep(SLEEP_TIME)

# Log Gagal
if failed:
    pd.DataFrame({"file_id": failed}).to_csv("../data/failed_downloads.csv", index=False)
    print(f"{len(failed)} lagu gagal. Lihat failed_downloads.csv")
else:
    print("Semua lirik berhasil diunduh.")
