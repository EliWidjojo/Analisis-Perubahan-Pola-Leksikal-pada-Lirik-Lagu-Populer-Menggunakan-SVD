from similaritas import (
    most_similar_cross_year,
    average_similarity_by_decade,
    decade_shift_distance
)

# Color
PINK = "\033[35m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

def menu():
    print(CYAN + "=============================================================================================")
    print(PINK + "Analisis Perubahan Pola Leksikal pada Lirik Lagu Populer di Amerika Serikat (1960–2025)")
    print(PINK + "Menggunakan Singular Value Decomposition (SVD)")
    print(CYAN + "=============================================================================================")
    print(GREEN + "- MENU -")
    print(GREEN + "1. Lagu paling mirip lintas tahun (most similar cross year)")
    print(GREEN + "2. Similaritas dalam dekade dan lintas dekade")
    print(GREEN + "3. Pergeseran leksikal antar dekade")
    print(GREEN + "4. Keluar")
    print(CYAN + "=============================================================================================" + RESET)

def main():
    while True:
        menu()
        pilihMenu = input("Masukkan pilihan (1-4): ")

        if pilihMenu == "1":
            tahun = int(input("Masukkan tahun (1960-2025): "))
            if (tahun < 1960 or tahun > 2025):
                print("Hanya ada data untuk tahun 1960 hingga 2025")
                continue

            print("\nHasil lagu paling mirip lintas tahun:\n")

            results = most_similar_cross_year(tahun)
            for r in results:
                print(
                    f"{r['source_doc']} ({r['source_year']})  -->  "
                    f"{r['most_similar_doc']} ({r['target_year']})  |  "
                    f"similarity = {r['similarity']:.4f}"
                ) 

        elif pilihMenu == "2":
            print("Perbandingan similaritas dalam dekade dan lintas dekade:")

            avg = average_similarity_by_decade()
            print(f"Dalam dekade yang sama : {avg['within_decade_avg']:.4f}")
            print(f"Lintas dekade          : {avg['cross_decade_avg']:.4f}")

        elif pilihMenu == "3":
            print("Pergeseran leksikal antar dekade:")

            shifts = decade_shift_distance()
            for s in shifts:
                print(
                    f"{s['from']} -> {s['to']}  |  "
                    f"jarak pergeseran = {s['distance']:.4f}"
                )

        elif pilihMenu == "4":
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

        input("\nTekan ENTER untuk kembali ke menu...")

if __name__ == "__main__":
    main()
