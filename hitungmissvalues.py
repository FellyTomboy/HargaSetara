import os
import pandas as pd

# === PATH KE FOLDER KONSUMEN DAN PRODUSEN ===
folder_konsumen = r"D:\LOMBA\HargaSetara\Data Panel Harga\B. Data Harga Konsumen 16 Maret 2021 - 12 Desember 2024\Jawa Timur"
folder_produsen = r"D:\LOMBA\HargaSetara\Data Panel Harga\A. Data Harga Produsen 16 Maret 2021 - 12 Desember 2024\Jawa Timur"

# === FUNGSI UNTUK MEMPROSES SEMUA FILE CSV DI SUATU FOLDER ===
def hitung_missing_values(folder_path, sumber):
    hasil = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            komoditas = os.path.splitext(file)[0]  # Nama file = nama komoditas
            try:
                df = pd.read_csv(file_path)
                missing = df['Harga'].isna().sum()
                hasil.append((komoditas, missing, sumber))
            except Exception as e:
                print(f"Gagal membaca {file}: {e}")
    return hasil

# === HITUNG MISSING VALUES DI KEDUA FOLDER ===
missing_konsumen = hitung_missing_values(folder_konsumen, "Konsumen")
missing_produsen = hitung_missing_values(folder_produsen, "Produsen")

# Gabungkan dan buat DataFrame
df_missing = pd.DataFrame(
    missing_konsumen + missing_produsen,
    columns=["Komoditas", "Missing Values", "Sumber"]
).sort_values(by="Missing Values", ascending=False)

# Tampilkan hasil
print(df_missing.to_string(index=False))
