import streamlit as st
import pandas as pd

# Excel sayfasını ve başlık satırını belirt
try:
    df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)
except Exception as e:
    st.error(f"Dosya yüklenemedi: {e}")
    st.stop()

# Kolonları normalize et
df.columns = df.columns.str.strip().str.upper()

# Kolon listesini göster (debug)
st.write("Kolonlar:", df.columns.tolist())

# Gerekli kolonlar gerçekten var mı
required_cols = ["GÖREV", "SÜRÜCÜ", "TARİH"]
missing = [col for col in required_cols if col not in df.columns]
if missing:
    st.error(f"Eksik kolonlar: {missing}")
    st.stop()

# Filtre verilerini alırken güvenlik kontrolü
try:
    gorev_list = sorted(df["GÖREV"].dropna().unique())
    surucu_list = sorted(df["SÜRÜCÜ"].dropna().unique())
    tarih_list = sorted(df["TARİH"].dropna().unique())
except Exception as e:
    st.error(f"Filtre listeleri oluşturulamadı: {e}")
    st.stop()

# Filtre bileşenleri
st.sidebar.header("Filtreler")
selected_gorev = st.sidebar.multiselect("Görev", gorev_list)
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_list)
selected_tarih = st.sidebar.multiselect("Tarih", tarih_list)

# Filtreleme
filtered_df = df.copy()
if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]
if selected_tarih:
    filtered_df = filtered_df[filtered_df["TARİH"].isin(selected_tarih)]

# Görüntülenecek kolonlar
display_cols = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
                "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "TOPLAM PAX"]
available_cols = [col for col in display_cols if col in filtered_df.columns]

# Raporu göster
st.title("Transfer İş Takibi Raporu")
st.dataframe(filtered_df[available_cols])
