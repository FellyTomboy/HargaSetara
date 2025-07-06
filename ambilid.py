import requests

url = "https://api-panelhargav2.badanpangan.go.id/api/front/komoditas"
headers = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
data = response.json()

komoditas_list = []

if data.get("status") == "success":
    for item in data.get("data", []):
        komoditas_id = int(item.get("id"))
        nama = item.get("nama")
        setting = item.get("setting_harga", [])
        
        # Ambil semua level_harga_id unik dari setting_harga
        level_ids = set()
        for s in setting:
            level_id = s.get("level_harga_id")
            if level_id:
                level_ids.add(int(level_id))
        
        if not level_ids:
            level_ids.add(-1)  # fallback jika tidak ada info
        
        komoditas_list.append((komoditas_id, nama, list(level_ids)))
        print(f"{komoditas_id}: {nama} -> Level Harga: {list(level_ids)}")
else:
    print("Gagal mengambil data komoditas.")
