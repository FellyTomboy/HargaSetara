import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()

params_template = {
    "period_date": "04/06/2025 - 17/06/2025",
    "level_harga_id": 1,
    "komoditas_id": 5
}

url = "https://api-panelhargav2.badanpangan.go.id/api/front/table-rekapitulasi-komoditas"

def extract_nama_fields(obj, prefix=''):
    """ Rekursif: ambil semua key yang mengandung nama/name dari nested dict/list """
    results = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if 'nama' in key.lower() or 'name' in key.lower():
                results.append((f"{prefix}{key}", value))
            if isinstance(value, (dict, list)):
                results.extend(extract_nama_fields(value, prefix=f"{prefix}{key}."))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            results.extend(extract_nama_fields(item, prefix=f"{prefix}[{idx}]."))
    return results

print("Daftar field nama dari province_id 1-200:\n")
for prov_id in range(1, 201):
    params = params_template.copy()
    params["province_id"] = prov_id
    
    try:
        resp = session.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()

        if data.get("status") == "success" and data.get("data"):
            first_entry = data["data"][0]
            nama_fields = extract_nama_fields(first_entry)

            if nama_fields:
                print(f"\nprovince_id {prov_id}:")
                for field, value in nama_fields:
                    print(f"  {field} = {value}")

    except Exception:
        continue  # Skip jika gagal koneksi atau parsing
