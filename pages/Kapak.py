import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# 📁 Excel verisini yükle
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)
df.columns = df.columns.str.strip().str.upper()
df["TARİH"] = pd.to_datetime(df["TARİH"], format="%d.%m.%Y", errors="coerce")

# 📅 Tarih filtresi (sidebar)
today = date.today()
st.sidebar.header("🔎 Filtreler")
start_date = st.sidebar.date_input("Başlangıç Tarihi", value=today)
end_date = st.sidebar.date_input("Bitiş Tarihi", value=today)

# 🔍 Tarih aralığına göre filtrele
filtered_df = df[(df["TARİH"].dt.date >= start_date) & (df["TARİH"].dt.date <= end_date)].copy()
filtered_df["TARİH"] = filtered_df["TARİH"].dt.strftime("%d.%m.%Y")

# 🚗 Plaka filtresi (ARAÇ)
arac_list = sorted(filtered_df["ARAÇ"].dropna().astype(str).unique())
selected_arac = st.sidebar.multiselect("Plaka (Araç)", arac_list)
if selected_arac:
    filtered_df = filtered_df[filtered_df["ARAÇ"].isin(selected_arac)]

# 🧑‍✈️ Sürücü filtresi
surucu_list = sorted(filtered_df["SÜRÜCÜ"].dropna().astype(str).unique())
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_list)
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]

# 📊 Tabloyu göster
display_cols = ["TARİH", "ARAÇ", "SAAT", "SÜRÜCÜ", "GÖREV", "OTEL", "TERMINAL", "PAX", "UÇUS KODU"]
valid_cols = [col for col in display_cols if col in filtered_df.columns]
st.title("🚐 Transfer İş Takibi Raporu")
st.dataframe(filtered_df[valid_cols])

# 🧾 WhatsApp için biçimlendirilmiş metni oluştur
def format_as_whatsapp_table(df):
    lines = [
        "🚐 Transfer Raporu",
        f"Tarih aralığı: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}",
        f"Toplam kayıt: {len(df)}",
        "",
        "ARAÇ       | SAAT   | SÜRÜCÜ      | GÖREV       | OTEL              | TERMİNAL | PAX",
        "-----------|--------|-------------|-------------|-------------------|----------|-----"
    ]
    for _, row in df.iterrows():
        line = f"{str(row['ARAÇ'])[:11]:<11} | {str(row['SAAT'])[:5]:<6} | {str(row['SÜRÜCÜ'])[:11]:<11} | {str(row['GÖREV'])[:11]:<11} | {str(row['OTEL'])[:19]:<19} | {str(row['TERMINAL'])[:8]:<8} | {str(row['PAX'])}"
        lines.append(line)
    return "\n".join(lines)

# 📲 WhatsApp mesajı oluştur
whatsapp_message = format_as_whatsapp_table(filtered_df[valid_cols])
encoded = urllib.parse.quote(whatsapp_message)
whatsapp_url = f"https://wa.me/?text={encoded}"

# 🔘 Gönder butonu
if st.button("📲 WhatsApp'ta Paylaş"):
    st.markdown(f"[👉 Mesajı WhatsApp'ta Aç]({whatsapp_url})", unsafe_allow_html=True)
