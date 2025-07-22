import streamlit as st
import pandas as pd
from datetime import datetime, date

# 📁 Excel verisini yükle
df = pd.read_excel("data/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)
df.columns = df.columns.str.strip().str.upper()

# 📅 Tarih seçimi (takvim arayüzü)
selected_date = st.sidebar.date_input("Rapor Tarihi", value=date.today())
formatted_date = selected_date.strftime("%d.%m.%Y")

# 🔍 Seçilen tarihe ait veriyi filtrele
df["TARİH"] = pd.to_datetime(df["TARİH"], format="%d.%m.%Y", errors="coerce")
filtered_df = df[df["TARİH"].dt.date == selected_date]

# 🚐 Plaka listesi
plakalar = filtered_df["ARAÇ"].dropna().astype(str).unique()

# 📊 Gösterilecek kolonlar
display_cols = ["SAAT", "GÖREV", "OTEL", "TERMINAL", "PAX", "UÇUS KODU"]

# 📋 Her araç için sabit tablo
st.title(f"🗓️ {formatted_date} - Araç Bazlı Görev Raporu")
for plaka in plakalar:
    arac_df = filtered_df[filtered_df["ARAÇ"] == plaka][display_cols]
    total_pax = arac_df["PAX"].sum() if "PAX" in arac_df.columns else 0
    total_task = len(arac_df)

    st.markdown(f"---")
    st.subheader(f"🚌 {plaka}")
    st.markdown(f"**Görev Sayısı:** {total_task} &nbsp;&nbsp;|&nbsp;&nbsp; **Toplam PAX:** {total_pax}")
    st.dataframe(arac_df.style.set_properties(**{"font-size": "12px"}))
