import streamlit as st
import pandas as pd
from datetime import datetime, date

# 📁 Excel dosyasını yükle
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)

# 🔡 Kolonları normalize et
df.columns = df.columns.str.strip().str.upper()
df["TARİH"] = pd.to_datetime(df["TARİH"], format="%d.%m.%Y", errors="coerce")

# ⏳ Bugünün tarihini al
today = date.today()

# 🎛️ Sidebar filtreler
st.sidebar.header("🔎 Filtreler")

# 1️⃣ Takvim ile tarih aralığı seçimi
start_date = st.sidebar.date_input("Başlangıç Tarihi", value=today)
end_date = st.sidebar.date_input("Bitiş Tarihi", value=today)

# 🧮 Tarihe göre veriyi filtrele
filtered_df = df[(df["TARİH"].dt.date >= start_date) & (df["TARİH"].dt.date <= end_date)]

# 2️⃣ Görev filtresi (seçilen tarihlere göre daraltılır)
gorev_options = sorted(filtered_df["GÖREV"].dropna().astype(str).unique())
selected_gorev = st.sidebar.multiselect("Görev", gorev_options)

if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]

# 3️⃣ Sürücü filtresi (seçilen görev ve tarihlere göre daraltılır)
surucu_options = sorted(filtered_df["SÜRÜCÜ"].dropna().astype(str).unique())
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_options)

if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]

# 📊 Rapor tablosu
st.title("🚐 Transfer İş Takibi Raporu")

display_cols = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
                "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]

valid_cols = [col for col in display_cols if col in filtered_df.columns]
st.dataframe(filtered_df[valid_cols])
