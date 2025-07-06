import os
import time
import requests
import calendar
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# === KONFIGURASI ===
base_dir = r"D:\LOMBA\HargaSetara\Data Panel Harga"
os.makedirs(base_dir, exist_ok=True)

MAX_RETRY = 5
DELAY = 2  # Detik antar request
TIMEOUT = 30  # Timeout per permintaan

# === SESSION DENGAN RETRY ===
session = requests.Session()
retries = Retry(total=MAX_RETRY, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

headers = {
    "accept": "application/json",
    "origin": "https://panelharga.badanpangan.go.id",
    "referer": "https://panelharga.badanpangan.go.id/",
    "user-agent": "Mozilla/5.0"
}

url_api = "https://api-panelhargav2.badanpangan.go.id/api/front/table-rekapitulasi-komoditas/export"

level_map = {
    1: "A. Data Harga Produsen 16 Maret 2021 - 12 Desember 2024",
    3: "B. Data Harga Konsumen 16 Maret 2021 - 12 Desember 2024"
}

# --- KOMODITAS KHUSUS PER LEVEL (BERDASARKAN CUACA) ---
komoditas_konsumen = {
    27: "Beras Premium"
}

komoditas_produsen = {

}


provinsi_dict = {
    15: "Jawa Timur"
}

# === RENTANG WAKTU ===
start_year = 2021
start_month = 3
end_year = 2024
end_month = 12

# === LOG FILES ===
log_sukses = open("log_sukses.txt", "a", encoding="utf-8")
log_error = open("log_error.txt", "a", encoding="utf-8")

# === MAIN LOOP ===
for level_id, level_folder in level_map.items():
    for prov_id, prov_name in provinsi_dict.items():
        # Pilih daftar komoditas sesuai level
        if level_id == 3:
            komoditas_dict = komoditas_konsumen
        elif level_id == 1:
            komoditas_dict = komoditas_produsen
        else:
            continue  # Lewati level yang tidak dikenal

        for kom_id, kom_name in komoditas_dict.items():
            # Lanjutkan seperti biasa ...
            folder_path = os.path.join(base_dir, level_folder, prov_name, kom_name.replace("/", "_"))
            os.makedirs(folder_path, exist_ok=True)

            year = start_year
            month = start_month
            while (year < end_year) or (year == end_year and month <= end_month):

                # Tanggal awal & akhir bulan
                day_start = "16/03/2021" if year == 2021 and month == 3 else f"01/{month:02d}/{year}"
                last_day = 31 if (year == 2021 and month == 3) else calendar.monthrange(year, month)[1]
                day_end = f"{last_day:02d}/{month:02d}/{year}"
                period_str = f"{day_start} - {day_end}"

                # Nama file
                file_name = f"{day_start.replace('/', '-')}_{day_end.replace('/', '-')}.xlsx"
                file_path = os.path.join(folder_path, file_name)

                if os.path.exists(file_path):
                    print(f"[{prov_name}/{kom_name}] Lewati (sudah ada): {file_name}")
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Mengunduh: {file_name}")
                    params = {
                        "period_date": period_str,
                        "level_harga_id": level_id,
                        "province_id": prov_id,
                        "komoditas_id": kom_id
                    }

                    try:
                        resp = session.get(url_api, headers=headers, params=params, timeout=TIMEOUT)
                        resp.raise_for_status()
                        data = resp.json()

                        if data.get("status") == "success" and data.get("data"):
                            download_url = data["data"]
                            resp_file = session.get(download_url, timeout=TIMEOUT)
                            with open(file_path, "wb") as f:
                                f.write(resp_file.content)
                            print(f"✔️  {file_path}")
                            log_sukses.write(f"{file_path}\n")
                        else:
                            print(f"⚠️  Tidak ada data: {period_str}")
                            log_error.write(f"[TIDAK ADA DATA] {prov_name} | {kom_name} | {period_str}\n")

                    except Exception as e:
                        print(f"❌ Error {period_str}: {e}")
                        log_error.write(f"[ERROR] {prov_name} | {kom_name} | {period_str} | {e}\n")

                    time.sleep(DELAY)

                # Naik bulan
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1

# === TUTUP LOG ===
log_sukses.close()
log_error.close()

print("\n✅ Semua proses selesai.")
