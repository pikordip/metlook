import streamlit as st
import pandas as pd

# Excel dosyasını doğru sayfa ile oku
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)

# Kolon isimlerini normalize et
df.columns = df.columns.str.strip().str.upper()

# Gerekli kolonlar varsa devam et
required = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL", "TERMINAL",
            "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]
missing = [col for col in required if col not in df.columns]
if missing:
    st.error(f"Eksik kolonlar: {missing}")
    st.stop()

# Sidebar filtreler
st.sidebar.header("Filtreler")

# Dinamik filtre listeleri
gorev_options = df["GÖREV"].dropna().unique()
surucu_options = df["SÜRÜCÜ"].dropna().unique()
tarih_options = df["TARİH"].dropna().unique()

# Filtre seçimleri
selected_gorev = st.sidebar.multiselect("Görev", sorted(gorev_options))
selected_surucu = st.sidebar.multiselect("Sürücü", sorted(surucu_options))
selected_tarih = st.sidebar.multiselect("Tarih", sorted(tarih_options))

# Filtreleme
filtered_df = df.copy()
if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]
if selected_tarih:
    filtered_df = filtered_df[filtered_df["TARİH"].isin(selected_tarih)]

# Rapor başlığı
st.title("🔍 Transfer İş Takibi Raporu")

# İstenilen başlıklarla tabloyu göster
columns = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL", "TERMINAL",
           "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]
st.dataframe(filtered_df[columns])
