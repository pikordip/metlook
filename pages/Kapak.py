import streamlit as st
import pandas as pd
from datetime import datetime

# 📁 Dosya yükleme
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)
df.columns = df.columns.str.strip().str.upper()
df["TARİH"] = df["TARİH"].astype(str)

# 📆 Bugünün tarihi
today = datetime.today().strftime("%d.%m.%Y")

# 🔍 Filtre verilerini güvenli şekilde hazırla
def get_filtered_options(df, col, prev_filters={}):
    temp_df = df.copy()
    for key, selected in prev_filters.items():
        if selected:
            temp_df = temp_df[temp_df[key].astype(str).isin(selected)]
    return sorted(temp_df[col].dropna().astype(str).str.strip().unique())

# 🎛️ Sidebar filtreler (entegre sıralı yapı)
st.sidebar.header("🔎 Filtreler")

# 1. Tarih filtresi
tarih_options = get_filtered_options(df, "TARİH")
default_tarih = [today] if today in tarih_options else []
selected_tarih = st.sidebar.multiselect("Tarih", tarih_options, default=default_tarih)

# 2. Görev filtresi (sadece seçilen tarihlere göre)
gorev_options = get_filtered_options(df, "GÖREV", {"TARİH": selected_tarih})
selected_gorev = st.sidebar.multiselect("Görev", gorev_options)

# 3. Sürücü filtresi (seçilen tarih ve görevlere göre)
surucu_options = get_filtered_options(df, "SÜRÜCÜ", {"TARİH": selected_tarih, "GÖREV": selected_gorev})
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_options)

# 🧮 Filtreleri uygula
filtered_df = df.copy()
if selected_tarih:
    filtered_df = filtered_df[filtered_df["TARİH"].isin(selected_tarih)]
if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]

# 📊 Rapor
st.title("🚐 Transfer İş Takibi Raporu")
columns = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
           "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]
existing_cols = [col for col in columns if col in filtered_df.columns]
st.dataframe(filtered_df[existing_cols])
