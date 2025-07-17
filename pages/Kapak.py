import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io
import urllib.parse
from PIL import Image

# 📁 Veriyi oku
df = pd.read_excel("data/metbeds/IMPERIAL.xlsx", sheet_name="DAİLY 2025", header=0)
df.columns = df.columns.str.strip().str.upper()
df["TARİH"] = pd.to_datetime(df["TARİH"], format="%d.%m.%Y", errors="coerce")

# 📅 Tarih filtresi
today = date.today()
st.sidebar.header("🔎 Filtreler")
selected_date = st.sidebar.date_input("Tarih", value=today)
filtered_df = df[df["TARİH"].dt.date == selected_date]

# 🎯 Görüntülenecek kolonlar
cols = ["ARAÇ", "SAAT", "SÜRÜCÜ", "GÖREV", "OTEL", "TERMINAL", "PAX"]
valid_cols = [col for col in cols if col in filtered_df.columns]
data = filtered_df[valid_cols].copy()

# 🧾 Görsel olarak tabloyu oluştur
def create_table_image(df):
    fig, ax = plt.subplots(figsize=(12, 0.6 + len(df)*0.5))
    ax.axis('off')

    # Tablo stilini uygula
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        colLoc='center'
    )
    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Görseli belleğe kaydet
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

# 📸 Görseli oluştur ve göster
if not data.empty:
    st.subheader(f"📊 {selected_date.strftime('%d.%m.%Y')} Transfer Tablosu (Görsel)")
    img_buffer = create_table_image(data)
    st.image(Image.open(img_buffer), caption="Tablo Görseli")

    # 📥 İndirme butonu
    st.download_button(
        label="📥 Görseli İndir",
        data=img_buffer,
        file_name="transfer_tablosu.png",
        mime="image/png"
    )

    st.info("Görseli indirip WhatsApp Web veya mobil uygulamada direkt paylaşabilirsiniz.")
else:
    st.warning("Seçilen tarihte kayıt bulunamadı.")
