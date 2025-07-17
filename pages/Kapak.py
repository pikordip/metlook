import streamlit as st
import pandas as pd

# Excel sayfasını ve başlık satırını tanımla
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)

# Kolon isimlerini normalize et
df.columns = df.columns.str.strip().str.upper()

# Filtre kolonları gerçekten var mı kontrol et
required_cols = ["GÖREV", "SÜRÜCÜ", "TARİH"]
missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Eksik kolonlar: {missing}")
else:
    # Filtre verilerini oluştur
    surucu_list = df["SÜRÜCÜ"].dropna().unique()
    gorev_list = df["GÖREV"].dropna().unique()
    tarih_list = df["TARİH"].dropna().unique()

    # Filtre arayüzü
    st.sidebar.header("Filtreler")
    selected_gorev = st.sidebar.multiselect("Görev", sorted(gorev_list))
    selected_surucu = st.sidebar.multiselect("Sürücü", sorted(surucu_list))
    selected_tarih = st.sidebar.multiselect("Tarih", sorted(tarih_list))

    # Filtreyi uygula
    filtered_df = df.copy()
    if selected_gorev:
        filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]
    if selected_surucu:
        filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]
    if selected_tarih:
        filtered_df = filtered_df[filtered_df["TARİH"].isin(selected_tarih)]

    # Raporu göster
    st.title("Transfer İş Takibi Raporu")
    display_cols = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
                    "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "Toplam PAX"]
    valid_cols = [col for col in display_cols if col in filtered_df.columns]
    st.dataframe(filtered_df[valid_cols])
