import requests
import csv
from datetime import datetime
import time

# Daftar 38 kabupaten/kota Jawa Timur + koordinat tengah
wilayah_jatim = {
    "Kabupaten Pacitan": (-8.1941, 111.1054),
    "Kabupaten Ponorogo": (-7.8684, 111.4695),
    "Kabupaten Trenggalek": (-8.0503, 111.7082),
    "Kabupaten Tulungagung": (-8.0653, 111.9020),
    "Kabupaten Blitar": (-8.0940, 112.2350),
    "Kabupaten Kediri": (-7.8483, 112.0642),
    "Kabupaten Malang": (-8.2319, 112.6326),
    "Kabupaten Lumajang": (-8.1330, 113.2246),
    "Kabupaten Jember": (-8.2646, 113.7000),
    "Kabupaten Banyuwangi": (-8.2182, 114.3576),
    "Kabupaten Bondowoso": (-7.9652, 113.8201),
    "Kabupaten Situbondo": (-7.7057, 114.0097),
    "Kabupaten Probolinggo": (-7.7773, 113.2192),
    "Kabupaten Pasuruan": (-7.6924, 112.8198),
    "Kabupaten Sidoarjo": (-7.4468, 112.7183),
    "Kabupaten Mojokerto": (-7.4871, 112.4343),
    "Kabupaten Jombang": (-7.5454, 112.2331),
    "Kabupaten Nganjuk": (-7.6111, 111.9010),
    "Kabupaten Madiun": (-7.6212, 111.5113),
    "Kabupaten Magetan": (-7.6594, 111.3336),
    "Kabupaten Ngawi": (-7.4042, 111.4468),
    "Kabupaten Bojonegoro": (-7.1500, 111.8833),
    "Kabupaten Tuban": (-6.8950, 112.0500),
    "Kabupaten Lamongan": (-7.1185, 112.4196),
    "Kabupaten Gresik": (-7.1617, 112.6536),
    "Kabupaten Bangkalan": (-7.0452, 112.9009),
    "Kabupaten Sampang": (-7.1703, 113.2506),
    "Kabupaten Pamekasan": (-7.1062, 113.4785),
    "Kabupaten Sumenep": (-6.9265, 113.8644),
    "Kota Kediri": (-7.8166, 112.0114),
    "Kota Blitar": (-8.0954, 112.1688),
    "Kota Malang": (-7.9813, 112.6304),
    "Kota Probolinggo": (-7.7543, 113.2158),
    "Kota Pasuruan": (-7.6441, 112.9035),
    "Kota Mojokerto": (-7.4720, 112.4337),
    "Kota Madiun": (-7.6299, 111.5231),
    "Kota Surabaya": (-7.2575, 112.7521),
    "Kota Batu": (-7.8671, 112.5239)
}


start_date = "2021-03-16"
end_date = "2024-12-12"

# File CSV
with open("cuaca_jatim_2021_2025.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["tanggal", "jam", "kab_kota", "temperature_2m", "humidity_2m", "weather_code"])

    for nama, (lat, lon) in wilayah_jatim.items():
        print(f"Ambil data untuk {nama}...")
        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={lat}&longitude={lon}"
            f"&start_date={start_date}&end_date={end_date}"
            f"&hourly=temperature_2m,relative_humidity_2m,weathercode"
            f"&timezone=Asia%2FBangkok"
        )

        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()

            for i in range(len(data["hourly"]["time"])):
                dt = datetime.strptime(data["hourly"]["time"][i], "%Y-%m-%dT%H:%M")
                tanggal = dt.strftime("%Y-%m-%d")
                jam = dt.strftime("%H:%M")
                suhu = data["hourly"]["temperature_2m"][i]
                kelembaban = data["hourly"]["relative_humidity_2m"][i]
                kode_cuaca = data["hourly"]["weathercode"][i]
                writer.writerow([tanggal, jam, nama, suhu, kelembaban, kode_cuaca])

            time.sleep(1)  # Hindari banned dari Open-Meteo
        except Exception as e:
            print(f"Gagal mengambil data untuk {nama}: {e}")
