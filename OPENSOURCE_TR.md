# AllScrape Backend - Açık Kaynak

AllScrape Backend, FastAPI ile inşa edilmiş açık kaynaklı bir web scraping ve LLM-ready içerik çıkarma API'sidir.

## Lisans

Bu proje **GNU General Public License v3 (GPLv3)** ile lisanslanmıştır.

### Bu Ne Anlama Geliyor?

- ✅ Yazılımı serbestçe kullanabilir, değiştirebilir ve dağıtabilirsiniz
- ✅ Değişikliklerinizin kaynak kodunu erişime açmalısınız
- ✅ Türev eserlerin aynı GPLv3 lisansı kullanması gerekir
- ✅ Orijinal lisans ve telif hakkı bildirimini içermelisiniz
- ✅ Hiçbir garanti verilmez

Tam lisans ayrıntıları için [LICENSE](LICENSE) ve [GPLv3 Legal Text](https://www.gnu.org/licenses/gpl-3.0.html) bölümüne bakın.

## Katkıda Bulunma

Katkılarınızı bekliyoruz! Ayrıntılar için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun.

Tüm katkılar GPLv3 ile lisanslanır.

## Güvenlik

Güvenlik açıklarını sorumlu bir şekilde bildirin. Ayrıntılar için [SECURITY.md](SECURITY.md) bölümüne bakın.

## Davranış Kuralları

Bu proje bir [Davranış Kuralları](CODE_OF_CONDUCT.md) benimsemektedir.

## Özellikler

- 🔍 Tek URL scraping (çoklu çıktı formatı)
- 🌐 Web arama ve otomatik sonuç scraping
- 🤖 LLM-ready çıktı formatı
- 📊 Metadata çıkarma
- ⚡ Hızlı asynchronous işleme
- 🧹 Temiz metin çıkarma

## Hızlı Başlangıç

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows'ta: venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
python -m uvicorn app.main:app --reload
```

## Belgeler

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Destek

Sorular, sorunlar veya öneriler için GitHub issue açın.
