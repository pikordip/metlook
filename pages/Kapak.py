import streamlit as st
import pandas as pd
from datetime import datetime

# 📁 Excel'den sayfayı ve başlıkları doğru al
try:
    df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)
except Exception as e:
    st.error(f"Veri dosyası yüklenemedi: {e}")
    st.stop()

# 🔡 Kolon adlarını normalize et
df.columns = df.columns.str.strip().str.upper()

# 🔎 Gerekli kolonlar
columns_needed = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
                  "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]
missing = [col for col in columns_needed if col not in df.columns]
if missing:
    st.error(f"Eksik kolonlar: {missing}")
    st.stop()

# 📆 Bugünün tarihini al (format Excel'e göre düzenlenebilir)
today = datetime.today().strftime("%d.%m.%Y")  # Örn: "17.07.2025"
df["TARİH"] = df["TARİH"].astype(str)

# 🧼 Filtre verilerini alırken veri tipini kontrol et
def get_safe_unique(col):
    try:
        return sorted(df[col].dropna().astype(str).str.strip().unique())
    except Exception:
        return []

gorev_options = get_safe_unique("GÖREV")
surucu_options = get_safe_unique("SÜRÜCÜ")
tarih_options = get_safe_unique("TARİH")

# 🎛️ Sidebar filtre arayüzü
st.sidebar.header("🔎 Filtreler")
selected_gorev = st.sidebar.multiselect("Görev", gorev_options)
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_options)
selected_tarih = st.sidebar.multiselect("Tarih", tarih_options, default=[today] if today in tarih_options else [])

# 🔍 Filtre uygulama
filtered_df = df.copy()
if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].astype(str).isin(selected_gorev)]
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].astype(str).isin(selected_surucu)]
if selected_tarih:
    filtered_df = filtered_df[filtered_df["TARİH"].astype(str).isin(selected_tarih)]

# 📋 Raporu göster
st.title("🚐 Transfer İş Takibi Raporu")
columns_to_display = [col for col in columns_needed if col in filtered_df.columns]
st.dataframe(filtered_df[columns_to_display])
