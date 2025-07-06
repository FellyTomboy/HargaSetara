import os
import pandas as pd

# Path utama folder hasil scraping
base_path = r"D:\LOMBA\HargaSetara\Data Panel Harga"

# Fungsi untuk proses gabung data di setiap folder komoditas
def proses_komoditas(folder_komoditas):
    file_list = [f for f in os.listdir(folder_komoditas) if f.endswith(".xlsx")]
    if not file_list:
        print(f"⚠️  Tidak ada file Excel di {folder_komoditas}")
        return
    
    all_data = []
    for file in file_list:
        file_path = os.path.join(folder_komoditas, file)
        print(f"📄 Membaca: {file_path}")
        
        try:
            df = pd.read_excel(file_path, header=2)
        except Exception as e:
            print(f"❌ Gagal membaca {file}: {e}")
            continue

        df.columns = df.columns.astype(str)
        if "Kab/Kota" not in df.columns:
            df.columns.values[1] = "Kab/Kota"  # Pastikan kolom ke-2 adalah Kab/Kota

        if "No" in df.columns:
            df = df.drop(columns=["No"])

        df_long = df.melt(id_vars=["Kab/Kota"], var_name="Tanggal", value_name="Harga")

        try:
            df_long["Tanggal"] = pd.to_datetime(df_long["Tanggal"], dayfirst=True)
        except:
            pass

        df_long["Harga"] = df_long["Harga"].replace(0, pd.NA)
        all_data.append(df_long)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values(by=["Tanggal", "Kab/Kota"])
        final_df = final_df[["Tanggal", "Kab/Kota", "Harga"]]

        # Nama file output CSV
        komoditas_name = os.path.basename(folder_komoditas)
        output_file = os.path.join(folder_komoditas, f"data_{komoditas_name.lower().replace(' ', '_')}.csv")
        final_df.to_csv(output_file, index=False)
        print(f"✅ Disimpan ke: {output_file}")
    else:
        print(f"⚠️  Tidak ada data yang berhasil dibaca di {folder_komoditas}")

# Telusuri seluruh struktur folder
for level_folder in os.listdir(base_path):
    path_level = os.path.join(base_path, level_folder)
    if not os.path.isdir(path_level):
        continue

    for prov_folder in os.listdir(path_level):
        path_prov = os.path.join(path_level, prov_folder)
        if not os.path.isdir(path_prov):
            continue

        for komoditas_folder in os.listdir(path_prov):
            path_komoditas = os.path.join(path_prov, komoditas_folder)
            if os.path.isdir(path_komoditas):
                print(f"\n📦 Memproses: {komoditas_folder}")
                proses_komoditas(path_komoditas)

print("\n🎉 Semua komoditas selesai diproses!")
