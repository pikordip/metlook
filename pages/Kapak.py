import streamlit as st
import pandas as pd
from datetime import datetime, date

# 📁 Excel dosyasını yükle
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)

# 🔡 Kolonları normalize et
df.columns = df.columns.str.strip().str.upper()
df["TARİH"] = pd.to_datetime(df["TARİH"], format="%d.%m.%Y", errors="coerce")

# ⏳ Bugünün tarihi
today = date.today()

# 🎛️ Sidebar filtreler
st.sidebar.header("🔎 Filtreler")

# 1️⃣ Takvim ile tarih aralığı seçimi
start_date = st.sidebar.date_input("Başlangıç Tarihi", value=today)
end_date = st.sidebar.date_input("Bitiş Tarihi", value=today)

# 🧮 Tarihe göre veri filtrele
filtered_df = df[(df["TARİH"].dt.date >= start_date) & (df["TARİH"].dt.date <= end_date)]

# 2️⃣ SÜRÜCÜ filtresi
surucu_list = sorted(filtered_df["SÜRÜCÜ"].dropna().astype(str).unique())
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_list)
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]

# 3️⃣ GÖREV filtresi (sürücü ve tarihe göre daraltılır)
gorev_list = sorted(filtered_df["GÖREV"].dropna().astype(str).unique())
selected_gorev = st.sidebar.multiselect("Görev", gorev_list)
if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]

# 📊 Rapor başlığı
st.title("🚐 Transfer İş Takibi Raporu")

# 🎯 Gösterilecek kolonlar ve tarih formatı düzeltme
display_cols = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
                "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]

# Tarih formatını sadece tarih olacak şekilde biçimlendir
filtered_df["TARİH"] = filtered_df["TARİH"].dt.strftime("%d.%m.%Y")

# Sadece mevcut kolonları göster
valid_cols = [col for col in display_cols if col in filtered_df.columns]
st.dataframe(filtered_df[valid_cols])
