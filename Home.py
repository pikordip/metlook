import streamlit as st
from datetime import date

# 🏷️ Sayfa başlığı ve stil
st.set_page_config(page_title="Metlook | Ana Sayfa", page_icon="🚐", layout="centered")

# 📅 Bugünün tarihi
today = date.today().strftime("%d.%m.%Y")

# 🧭 Başlık
st.title("🚐 Metlook Transfer Takip Sistemi")
st.markdown(f"📅 **Bugünün Tarihi:** {today}")

# 📝 Açıklama
st.markdown("""
### Hoş geldiniz!

Bu uygulama, transfer operasyonlarınızı kolayca takip etmeniz, görevleri filtrelemeniz ve raporları hızlıca paylaşmanız için tasarlandı.

#### 🔍 Neler Yapabilirsiniz?
- **Transfer Raporu:** Tarih, sürücü ve araç bazlı filtreleme ile görev detaylarını görüntüleyin.
- **WhatsApp Paylaşımı:** Görev listesini tek tıkla mesaj olarak paylaşın.
- **PDF / Görsel Raporlar:** Tabloyu görsel veya dosya olarak dışa aktarın.
- **Görev Takibi:** Araç bazlı görev yoğunluğunu analiz edin.

#### 📂 Sayfa Modülleri:
- 📊 **Transfer Raporu:** Detaylı görev listesi ve filtreleme ekranı  
- 📲 **WhatsApp Paylaşımı:** Etiketli görev mesajları oluşturma  
- 🖼️ **Görsel Raporlar:** Tabloyu PNG olarak indirilebilir hale getirme  
- 📄 **PDF Raporu:** Kurumsal formatta dışa aktarım (isteğe bağlı)

---

### 🧠 İpuçları:
- Sol menüden istediğiniz modüle geçebilirsiniz.
- Filtreleri kullanarak sadece ilgili görevleri görüntüleyin.
- Paylaşım butonları ile ekip içi iletişimi hızlandırın.

---

Her türlü öneriniz veya geliştirme talebiniz için buradayız.  
İyi çalışmalar! 🚀
""")

