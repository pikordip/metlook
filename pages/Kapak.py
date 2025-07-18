import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse

# 📁 Excel verisi
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)
df.columns = df.columns.str.strip().str.upper()
df["TARİH"] = pd.to_datetime(df["TARİH"], format="%d.%m.%Y", errors="coerce")

# 📅 Sidebar filtreler
today = date.today()
st.sidebar.header("🔎 Filtreler")
selected_date = st.sidebar.date_input("Rapor Tarihi", value=today)

# 📆 Tarih filtresi (tek gün)
filtered_df = df[df["TARİH"].dt.date == selected_date].copy()
filtered_df["TARİH"] = filtered_df["TARİH"].dt.strftime("%d.%m.%Y")

# 🚗 Plaka filtresi
arac_list = sorted(filtered_df["ARAÇ"].dropna().astype(str).unique())
selected_arac = st.sidebar.multiselect("Plaka (ARAÇ)", arac_list)
if selected_arac:
    filtered_df = filtered_df[filtered_df["ARAÇ"].isin(selected_arac)]

# 👤 Sürücü filtresi
surucu_list = sorted(filtered_df["SÜRÜCÜ"].dropna().astype(str).unique())
selected_surucu = st.sidebar.multiselect("Sürücü", surucu_list)
if selected_surucu:
    filtered_df = filtered_df[filtered_df["SÜRÜCÜ"].isin(selected_surucu)]

# 📊 Görüntülenecek kolonlar
display_cols = ["TARİH", "SAAT", "ARAÇ", "SÜRÜCÜ", "ACENTA", "GÖREV", "OTEL",
                "TERMINAL", "UÇUS KODU", "GRUP NO", "MİSAFİR İSMİ", "PAX"]
valid_cols = [col for col in display_cols if col in filtered_df.columns]

# 🧮 Eğer veri varsa, özet ve tabloyu göster
if not filtered_df.empty:
    st.title("🚐 Transfer İş Takibi Raporu")

    # 🔢 Toplam bilgiler
    toplam_pax = filtered_df["PAX"].sum()
    toplam_arac = filtered_df["ARAÇ"].nunique()
    toplam_kayit = len(filtered_df)

    # 🔹 Yan yana gösterim
    col1, col2, col3 = st.columns(3)
    col1.metric("🔢 Toplam Kayıt", toplam_kayit)
    col2.metric("👥 Toplam PAX", toplam_pax)
    col3.metric("🚗 Araç Sayısı", toplam_arac)

    # 📋 Tabloyu göster
    st.dataframe(filtered_df[valid_cols])

    # 💬 WhatsApp mesaj formatı – etiketli satırlar
    def format_whatsapp_blocks(df):
        lines = [
            "🚐 Transfer Raporu",
            f"Tarih: {selected_date.strftime('%d.%m.%Y')}",
            f"Toplam kayıt: {len(df)}",
            ""
        ]
        for _, row in df.iterrows():
            blok = f"""Tarih: {row['TARİH']}
Saat: {row['SAAT']}
Plaka: {row['ARAÇ']}
Sürücü: {row['SÜRÜCÜ']}
Acenta: {row.get('ACENTA', '')}
Görev: {row['GÖREV']}
Otel: {row['OTEL']}
Terminal: {row['TERMINAL']}
Uçuş Kodu: {row.get('UÇUS KODU', '')}
Grup No: {row.get('GRUP NO', '')}
Misafir: {row.get('MİSAFİR İSMİ', '')}
PAX: {row['PAX']}
------------------------"""
            lines.append(blok)
        return "\n".join(lines)

    # 📲 WhatsApp mesajı oluştur
    message_text = format_whatsapp_blocks(filtered_df[valid_cols])
    encoded = urllib.parse.quote(message_text)
    whatsapp_url = f"https://wa.me/?text={encoded}"

    # 🔘 Paylaşım butonu
    if st.button("📲 WhatsApp'ta Paylaş"):
        st.markdown(f"[👉 Mesajı WhatsApp'ta Aç]({whatsapp_url})", unsafe_allow_html=True)

else:
    st.title("🚐 Transfer İş Takibi Raporu")
    st.warning(f"{selected_date.strftime('%d.%m.%Y')} tarihinde kayıt bulunamadı.")
    st.info("Lütfen farklı bir tarih seçerek tekrar deneyin.")
