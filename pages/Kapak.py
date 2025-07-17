import streamlit as st
import pandas as pd

# Veriyi yükle
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx")

# Kolon isimlerini normalize et (boşluk ve harf farklarını düzeltmek için)
df.columns = df.columns.str.strip().str.upper()

# Kolonları ekrana yazdır (debug için)
st.write("Kolonlar:", df.columns.tolist())

# GÖREV sütunu gerçekten varsa filtrelemeye geç
if "GÖREV" in df.columns and "SÜRÜCÜ" in df.columns and "TARİH" in df.columns:

    gorev_list = df["GÖREV"].dropna().unique()
    surucu_list = df["SÜRÜCÜ"].dropna().unique()
    tarih_list = df["TARİH"].dropna().unique()

    # Sidebar filtreler
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

    # Raporu göster
    st.title("Transfer İş Takibi Raporu")

    st.dataframe(filtered_df[
        ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL", "TERMINAL", 
         "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "Toplam PAX"]
    ])

else:
    st.error("GÖREV, SÜRÜCÜ veya TARİH kolonlarından biri bulunamadı. Lütfen Excel dosyasını kontrol et.")
