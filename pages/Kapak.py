import streamlit as st
import pandas as pd

# Veriyi yükle
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx")

# Kolon isimlerini normalize et
df.columns = df.columns.str.strip().str.upper()

# Mevcut kolonları göster (debug amacıyla)
st.write("Mevcut Kolonlar:", df.columns.tolist())

# Filtrelenecek kolonların gerçekten var olduğunu kontrol et
required_cols = ["GÖREV", "SÜRÜCÜ", "TARİH"]
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"Bu kolonlar eksik veya hatalı: {missing_cols}")
else:
    # Filtre listeleri
    gorev_list = df["GÖREV"].dropna().unique()
    surucu_list = df["SÜRÜCÜ"].dropna().unique()
    tarih_list = df["TARİH"].dropna().unique()

    # Filtreler
    st.sidebar.header("Filtreleme")
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
    columns_to_display = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
                          "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "Toplam PAX"]
    
    # Mevcut olan kolonları filtrele (eksik kolon varsa uygulama hata vermez)
    columns_available = [col for col in columns_to_display if col in filtered_df.columns]
    st.dataframe(filtered_df[columns_available])
