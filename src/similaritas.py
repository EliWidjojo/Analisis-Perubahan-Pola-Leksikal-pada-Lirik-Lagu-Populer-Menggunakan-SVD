import numpy as np
from read_mapper import load_texts
from term_document import tf_idf
from svd import svd

texts, labels = load_texts()
X, valid = tf_idf(texts)
labels = [labels[i] for i in range(len(labels)) if valid[i]]
doc_names = [l["file"] for l in labels]
years = np.array([l["year"] for l in labels])
assert X.shape[1] == len(labels)
U, S, Vt = svd(X, k=100)
D = Vt.T @ S
norms = np.linalg.norm(D, axis=1, keepdims=True)
D_norm = D / np.maximum(norms, 1e-10)
sim_matrix = D_norm @ D_norm.T

# Fungsi menemukan lagu paling mirip lintas tahun
def most_similar_cross_year(target_year):
    idx_src = np.where(years == target_year)[0]
    idx_oth = np.where(years != target_year)[0]

    results = []
    for i in idx_src:
        sims = sim_matrix[i, idx_oth]
        j = idx_oth[np.argmax(sims)]

        results.append({
            "source_doc": doc_names[i],
            "source_year": target_year,
            "most_similar_doc": doc_names[j],
            "target_year": int(years[j]),
            "similarity": float(sim_matrix[i, j])
        })
    return results

# Fungsi konversi tahun ke dekade, khusus 2021–2025
def year_to_decade(year):
    if year >= 2021:
        return 2025  # Dekade khusus 2021-2025
    return (year // 10) * 10

decades = np.array([year_to_decade(y) for y in years])

# Rata-rata similarity dalam dekade dan lintas dekade
def average_similarity_by_decade():
    within = []
    cross = []
    n = len(doc_names)
    for i in range(n):
        for j in range(i + 1, n):
            if decades[i] == decades[j]:
                within.append(sim_matrix[i, j])
            else:
                cross.append(sim_matrix[i, j])
    return {
        "within_decade_avg": float(np.mean(within)),
        "cross_decade_avg": float(np.mean(cross))
    }

# Centroid per dekade
def decade_centroids():
    centroids = {}
    for d in np.unique(decades):
        idx = np.where(decades == d)[0]
        centroids[d] = D_norm[idx, :2].mean(axis=0)
    return centroids

# Pergeseran leksikal antar dekade
def decade_shift_distance():
    centroids = decade_centroids()
    decs = sorted(centroids.keys())

    shifts = []
    for i in range(len(decs) - 1):
        d1, d2 = decs[i], decs[i + 1]
        dist = np.linalg.norm(centroids[d2] - centroids[d1])
        shifts.append({
            "from": d1,
            "to": d2,
            "distance": float(dist)
        })
    return shifts

if __name__ == "__main__":
    print("Pergeseran leksikal antar dekade:")
    for shift in decade_shift_distance():
        print(f"{shift['from']} -> {shift['to']}  |  jarak pergeseran = {shift['distance']:.4f}")
