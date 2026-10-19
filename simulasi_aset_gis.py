import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# ==========================================
# 1. SIMULASI DATA PELAPORAN LAPANGAN (CLOUD)
# ==========================================
# Menggambarkan data yang dikirim oleh tim survei/masyarakat (Longitude, Latitude)
laporan_aset = [
    {"id_laporan": "A01", "jenis": "Pohon Tumbang", "lat": -3.7955, "lon": 102.2591, "status": "Pending"},
    {"id_laporan": "A02", "jenis": "Lampu Jalan Mati", "lat": -3.7960, "lon": 102.2605, "status": "Pending"},
    {"id_laporan": "A03", "jenis": "Jalan Berlubang", "lat": -3.7940, "lon": 102.2580, "status": "In Progress"}
]

# Konversi ke DataFrame Pandas
df = pd.DataFrame(laporan_aset)

# ==========================================
# 2. PROSES GEOSPASIAL (Membuat Geometri Titik)
# ==========================================
# Membuat kolom geometri agar bisa dibaca sebagai data spasial
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

print("Data Spasial Berhasil Diproses (Simulasi PostGIS):")
print(gdf[['id_laporan', 'jenis', 'geometry']])

# ==========================================
# 3. WEB-GIS (Render Peta Otomatis Menggunakan Folium)
# ==========================================
# Pusat peta disetel di area Universitas Bengkulu / Kota Bengkulu
peta_aset = folium.Map(location=[-3.7950, 102.2590], zoom_start=16)

# Looping untuk memasukkan setiap titik laporan ke dalam peta
for idx, row in gdf.iterrows():
    # Menentukan warna berdasarkan jenis laporan
    color = "red" if row['jenis'] == "Pohon Tumbang" else "orange" if row['jenis'] == "Jalan Berlubang" else "blue"
    
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"ID: {row['id_laporan']}<br>Jenis: {row['jenis']}<br>Status: {row['status']}",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(peta_aset)

# Menyimpan hasil peta menjadi file HTML interaktif (Selesai diproses)
nama_file = "peta_laporan_aset.html"
peta_aset.save(nama_file)
print(f"\nPeta berhasil di-generate! Buka file '{nama_file}' di browser Anda untuk melihat hasilnya.")