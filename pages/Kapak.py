import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# 📁 Excel dosyasını yükle
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)
df.columns = df.columns.str.strip().str.upper()
df["TARİH"] = pd.to_datetime(df["TARİH"], format="%d.%m.%Y", errors="coerce")

# 📅 Tarih seçimi
today = date.today()
st.sidebar.header("🔎 Filtreler")
start_date = st.sidebar.date_input("Başlangıç Tarihi", value=today)
end_date = st.sidebar.date_input("Bitiş Tarihi", value=today)

# 🔍 Tarih aralığında veri filtrele
filtered_df = df[(df["TARİH"].dt.date >= start_date) & (df["TARİH"].dt.date <= end_date)]

# 🚗 SÜRÜCÜ filtresi
surucu_list = sorted(filtered_df["SÜRÜCÜ"].dropna().astype(str).unique())
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_list)
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]

# 📝 GÖREV filtresi
gorev_list = sorted(filtered_df["GÖREV"].dropna().astype(str).unique())
selected_gorev = st.sidebar.multiselect("Görev", gorev_list)
if selected_gorev:
    filtered_df = filtered_df[filtered_df["GÖREV"].isin(selected_gorev)]

# 📊 Rapor başlığı ve tablo
st.title("🚐 Transfer İş Takibi Raporu")

# Tarihi yalnızca gün/ay/yıl formatında göster
filtered_df["TARİH"] = filtered_df["TARİH"].dt.strftime("%d.%m.%Y")

# Görüntülenecek kolonlar
display_cols = ["TARİH", "ARAÇ", "SÜRÜCÜ", "SAAT", "ACENTA", "GÖREV", "OTEL",
                "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]
valid_cols = [col for col in display_cols if col in filtered_df.columns]
st.dataframe(filtered_df[valid_cols])

# 📲 WhatsApp mesajı oluştur
summary = f"Transfer raporu hazır.\nTarih aralığı: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}\nToplam kayıt: {len(filtered_df)}"
encoded_message = urllib.parse.quote(summary)
whatsapp_url = f"https://wa.me/?text={encoded_message}"

# Buton ve bağlantı
if st.button("📲 WhatsApp'ta Paylaş"):
    st.markdown(f"[👉 Mesajı WhatsApp'ta Aç]({whatsapp_url})", unsafe_allow_html=True)
