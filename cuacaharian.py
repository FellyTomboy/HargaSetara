import pandas as pd

# Baca data
df = pd.read_csv('cuaca_jatim_2021_2025.csv', parse_dates=['tanggal'])
df['jam_int'] = pd.to_datetime(df['jam'], format='%H:%M').dt.hour

# Deteksi hujan & intensitas
def is_rain(code):
    return code in [51, 53, 55, 61, 63, 65, 80, 81, 82]

def rain_severity(code):
    if code in [51, 61, 80]:
        return 1
    elif code in [53, 63, 81]:
        return 2
    elif code in [55, 65, 82]:
        return 3
    return 0

df['rainy'] = df['weather_code'].apply(is_rain)
df['rain_score'] = df['weather_code'].apply(rain_severity)
df['is_daytime'] = df['jam_int'].between(6, 18)

# Agregasi harian
agg = df.groupby(['tanggal', 'kab_kota']).agg(
    suhu_avg=('temperature_2m', 'mean'),
    suhu_max=('temperature_2m', 'max'),
    suhu_min=('temperature_2m', 'min'),
    kelembaban_avg=('humidity_2m', 'mean'),
    rainy_hours=('rainy', 'sum'),
    rain_score=('rain_score', 'sum'),
    rainy_hours_day=('rainy', lambda x: x[df.loc[x.index, 'is_daytime']].sum()),
    dominant_weather_code=('weather_code', lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0])
).reset_index()

# Rolling window otomatis (mean vs sum)
rolling_days = [3, 7, 30]
rolling_features = {
    'suhu_avg': 'mean',
    'suhu_max': 'mean',
    'suhu_min': 'mean',
    'kelembaban_avg': 'mean',
    'rainy_hours': 'sum',
    'rain_score': 'sum',
    'rainy_hours_day': 'sum'
}

for col, method in rolling_features.items():
    for window in rolling_days:
        new_col = f'{col}_roll{window}d'
        if method == 'mean':
            agg[new_col] = (
                agg.sort_values('tanggal')
                   .groupby('kab_kota')[col]
                   .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
            )
        elif method == 'sum':
            agg[new_col] = (
                agg.sort_values('tanggal')
                   .groupby('kab_kota')[col]
                   .transform(lambda x: x.rolling(window=window, min_periods=1).sum())
            )

# Simpan ke CSV
agg.to_csv("cuaca_agregat.csv", index=False)

# Cek hasil
print("✅ Data agregasi cuaca telah disimpan ke cuaca_agregat.csv")
print(agg.head())
