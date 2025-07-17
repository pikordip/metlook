import streamlit as st
import pandas as pd
from datetime import datetime

# 🔹 Veriyi yükle
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)

# 🔹 Kolon isimlerini normalize et
df.columns = df.columns.str.strip().str.upper()

# 🔹 Bugünün tarihini al (format: gün/ay/yıl veya dosyaya uygun biçimde ayarla)
today_str = datetime.today().strftime("%d.%m.%Y")  # Örnek: "17.07.2025"

# 🔹 Tarama için filtre listeleri oluştur
gorev_list = sorted(df["GÖREV"].dropna().unique())
surucu_list = sorted(df["SÜRÜCÜ"].dropna().unique())
tarih_list = sorted(df["TARİH"].dropna().astype(str).unique())

# 🔹 Sidebar filtreler
st.sidebar.header("🔎 Filtreler")

selected_gorev = st.sidebar.multiselect("Görev", gorev_list)
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_list)

# 🔹 Tarih filtresi – bugünün tarihi varsayılan seçili
if today_str in tarih_list:
    selected_tarih = st.sidebar.multiselect("Tarih", tarih_list, default=[today_str])
else:
    selected_tarih = st.sidebar.multiselect("Tarih", tarih_list)

# 🔹 Filtreleme işlemi
filtered_df = df.copy()

if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]
if selected_tarih:
    filtered_df = filtered_df[df["TARİH"].astype(str).isin(selected_tarih)]

# 🔹 Rapor başlığı
st.title("📋 Transfer İş Takibi Raporu")

# 🔹 Gösterilecek kolonlar
columns = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
           "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]

existing_cols = [col for col in columns if col in filtered_df.columns]
st.dataframe(filtered_df[existing_cols])
