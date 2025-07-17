import streamlit as st
import pandas as pd

# Veriyi yükle
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx")

# Kolon isimlerini düzenle (gerekirse başlıklarla uyumlu hale getir)
df.columns = [col.strip().upper() for col in df.columns]

# Filtre alanları
gorev_list = df["GÖREV"].dropna().unique()
surucu_list = df["SÜRÜCÜ"].dropna().unique()
tarih_list = df["TARİH"].dropna().unique()

# Sidebar filtreleri
st.sidebar.header("Filtrele")
selected_gorev = st.sidebar.multiselect("Görev", sorted(gorev_list))
selected_surucu = st.sidebar.multiselect("Sürücü", sorted(surucu_list))
selected_tarih = st.sidebar.multiselect("Tarih", sorted(tarih_list))

# Filtreleme işlemi
filtered_df = df.copy()

if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]
if selected_tarih:
    filtered_df = filtered_df[filtered_df["TARİH"].isin(selected_tarih)]

# Rapor başlığı
st.title("Transfer İş Takibi Raporu")

# Tabloyu göster
st.dataframe(filtered_df[
    ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL", "TERMINAL", 
     "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "Toplam PAX"]
])
