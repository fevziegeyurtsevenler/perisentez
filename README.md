<p align="center">
  <img src="https://raw.githubusercontent.com/fevziegeyurtsevenler/perisentez/main/logo.jpeg" width="250" alt="Perisentez Logo"/>
</p>

# Perisentez

## 👥 Takım İsmi
**Timpossible**

## 👩‍💻 Takım Elemanları

| Name                   | Title          | Social                                                                 |
| :--------------------- | :------------- | :--------------------------------------------------------------------- |
| Feyza Hilal Şahin      | Product Owner  | [LinkedIn](https://tr.linkedin.com/in/feyza-hilal-%C5%9Fahin-153989210) |
| Fevzi Ege Yurtsevenler | Scrum Master   | [LinkedIn](https://www.linkedin.com/in/fevziege/)                      |
| Sena Açıkgöz           | Developer      | [LinkedIn](https://www.linkedin.com/in/sena-açıkgöz00)                 |
| Semanur Büdün          | Developer      | [LinkedIn](https://www.linkedin.com/in/semanur-budun)                  |
| Tarık Anafarta         | Developer      | [LinkedIn](https://www.linkedin.com/in/tarik-anafarta)                 |

---

## 🧬 Ürün İsmi
**Perisentez**

## 📖 Ürün Açıklaması
Perisentez, prenatal (doğum öncesi) dönemde ultrason ve serum bulgularına göre genetik sendrom tahmini yaparak, uzman hekimlere karar desteği sunan **yapay zekâ tabanlı bir asistan sistemidir**.  

Uygulama, hekimin girdiği bulguları makine öğrenmesi modeliyle değerlendirir, olası sendromları güven oranlarıyla sıralar ve yapay zekâ açıklamaları ile hekimlere karar sürecinde rehberlik eder.  

**Google Gemini** entegrasyonu sayesinde hekimler uygulama içinden medikal danışmanlık alabilir. Ayrıca **HTML tabanlı modern raporlama** ile hasta sonuçları renk kodlu risk etiketleriyle sunulup kolayca paylaşılabilir hale gelmiştir.  

Uygulama, artık sadece prototip değil; klinik kullanıma hazır bir **karar destek sistemi**dir.  

---

## 🔑 Ürün Özellikleri
- **Prenatal Veri Girişi**
  - Gebelik haftası, ense kalınlığı (NT), femur uzunluğu (FL), β-hCG ve PAPP-A değerleri girilebilir.
  - Önemli yapısal anomaliler listeden seçilebilir (ör. Omfalosel, Holoprozensefali, Kardiyak defekt).

- **Makine Öğrenmesi ile Risk Analizi**
  - Girilen bulgular ML modeli ile işlenir, olası sendromlar güven oranları ile listelenir.

- **Yapay Zekâ Açıklama Modülü**
  - Bulgular için neden-sonuç ilişkisi açıklar.
  - Risk faktörleri rapora eklenir.

- **Gemini & GPT Chatbot**
  - Prenatal sendromlarla ilgili tıbbi danışmanlık sağlar.
  - Hekimlere ek bilgi desteği sunar.

- **Modern HTML Raporlama**
  - Renk kodlu risk etiketleri ile açıklayıcı raporlar hazırlanır.
  - Raporlar indirilebilir ve paylaşılabilir.

- **Hasta Geçmişi Yönetimi**
  - SQLite veritabanında kullanıcı bazlı kayıtlar saklanır.
  - Geçmiş raporlara erişim ve indirme desteği bulunur.

---

## 🎯 Hedef Kitle
- Perinatoloji uzmanları  
- Kadın doğum doktorları  
- Tıp fakültesi öğrencileri  
- Genetik danışmanlar  
- Medikal AI sistemleri geliştirmek isteyen araştırmacılar
- Radyoloji Uzmanları

---

## 📌 Product Backlog
[📌 Trello Backlog](https://trello.com/b/U1T5wQXG/prenatal-diagnosis-ai)

---

## 🧑‍⚕️ User Story
**Kullanıcı Tipi:** Perinatoloji Uzmanı (Dr. Şeyda)  

“Bir perinatoloji uzmanı olarak, detaylı ultrason muayenesinde tespit ettiğim fetal bulguları sisteme girerek bu bulgularla en çok eşleşen genetik sendromların listesini görmek istiyorum. Böylece olası tanıları daha hızlı değerlendirebilir ve hastaya en uygun ileri test ve yönlendirmeyi yapabilirim.”

**Kabul Kriterleri:**
- Arama çubuğunda otomatik tamamlama
- Girilen bulguların standart tıbbi terimlere dönüştürülmesi
- İlk 3 olası sendromun güven oranları ile listelenmesi
- ICD kodları ve fenotip açıklamaları
- Hangi bulgularla eşleştiğinin belirtilmesi

---

## 🚀 Kullanım
🔗 [Perisentez Uygulamasını Deneyin](https://perisentez.streamlit.app/)  

📘 [Perisentez Kullanım Kılavuzu (PDF)](https://github.com/fevziegeyurtsevenler/perisentez/raw/main/kullanim_kilavuzu.pdf)

🎥 [Perisentez Tanıtım Videosu (YouTube)](https://www.youtube.com/watch?v=br2Xd0sz3Hs)

📄 [Sendrom Açıklamaları (PDF)](https://github.com/fevziegeyurtsevenler/perisentez/raw/main/sendrom_aciklama.pdf)

---

# 📌 Sprint 1

## Sprint Amacı
Minimum Uygulanabilir Ürün (MVP) geliştirilmesi: temel veri girişi, kural tabanlı risk hesaplama ve prototip arayüz.

## Sprint Notları
- **UI Tasarımları:** Streamlit kütüphanesi ile doğrudan kodlandı.  
- **Proje Yönetimi:** Trello ile takip edildi.  
- **Günlük Scrum Toplantıları:** WhatsApp + Google Meet.  
- **Uygulama Teması:** Koyu (dark).  
- **Dil:** Türkçe.  

## Beklenen Puan Tamamlama
- **Sprint 1 Hedefi:** 300 Puan  
- **Puan Tamamlama Mantığı:**  
  - Projenin genel hedefi 1200 puan.  
  - Sprint 1 → MVP: 300 puan  
  - Sprint 2 → Model & entegrasyon: 450 puan  
  - Sprint 3 → Son geliştirmeler & teslim: 450 puan  
- **Tamamlanan:** 300 Puan ✅ (Tam Puan)  

## Günlük Scrumlar
- Günlük ilerleme paylaşımları WhatsApp üzerinden, detaylı tartışmalar Google Meet ile yapıldı.

## Sprint Değerlendirmesi (Sprint Review)
- ✅ Fetal bulgular girişi  
- ✅ Kural tabanlı risk analizi  
- ✅ Sendrom sıralama  
- ✅ Açıklayıcı bilgilendirme  

**Karşılaşılan Zorluklar ve Çıkarımlar**
- AI tanımını MVP kural tabanlı sistemle dengeleme tartışıldı.  
- Klinik karara destek misyonu vurgulandı.  

**Sprint Değerlendirmesi Katılımcıları**
- Feyza Hilal Şahin  
- Fevzi Ege Yurtsevenler  
- Sena Açıkgöz  
- Semanur Büdün  
- Tarık Anafarta  

## Ekran Görüntüleri ve Kullanım Videosu
[Ekran Görüntüleri Albümü](https://imgur.com/a/Bc1tRcg)

## Sprint Retrospektifi
- Firebase araştırılması  
- Logo & marka kimliği oluşturulması  
- AI API entegrasyonu planlanması  

---

# 📌 Sprint 2

## Sprint Amacı
MVP üzerine makine öğrenmesi modeli, hasta geçmişi yönetimi, PDF raporlama ve yapay zekâ açıklama modülü ekleyerek klinik kullanıma daha uygun hale getirmek.

## Sprint Notları
- 🔍 **Makine Öğrenmesi Modeli Entegrasyonu**  
- 🧠 **Yapay Zekâ Yorumlayıcı Modül**  
- 📄 **PDF Raporlama Özelliği**  
- 💾 **SQLite Hasta Veritabanı**  
- 🔐 **Giriş / Kayıt Sistemi**  
- 🗂️ **Hasta Geçmişi Paneli**

## Beklenen Puan Tamamlama
- **Sprint 2 Hedefi:** 450 Puan  
- **Tamamlanan Tahmini Puan:** 470 Puan ✅  
- **Dağılım:**  
  - ML modeli + veri yönetimi: 200 puan  
  - PDF raporlama + grafikler: 120 puan  
  - Kullanıcı yönetimi + geçmiş: 100 puan  
  - Bonus (AI açıklama modülü & görsel iyileştirme): 50 puan  

## Günlük Scrumlar
- WhatsApp + Google Meet  
- PDF ve AI modülü canlı demo ile test edildi  

## Ekran Görüntüleri
[Ekran Görüntüleri Albümü](https://imgur.com/a/wUub993)

## Sprint Retrospektifi
- Veriler kalıcı ve güvenli hale geldi  
- Sistem neden-sonuç ilişkilerini açıklıyor  
- UI/UX geliştirildi  

---

# 📌 Sprint 3

## Sprint Amacı
AI entegrasyonu, HTML raporlama ve kullanıcı deneyimi iyileştirmeleriyle ürünü klinik kullanıma hazır hale getirmek.

## Sprint Notları
- 📄 PDF yerine **HTML raporlama sistemi**  
- 🤖 **Gemini entegrasyonu**  
- 🧠 **Geliştirilmiş yapay zekâ açıklama modülü**  
- 🎨 **UI iyileştirmeleri** (risk etiketleri, modern tasarım)  
- 💾 **SQLite hasta geçmişi ve güvenlik**

## Beklenen Puan Tamamlama
- **Sprint 3 Hedefi:** 450 Puan  
- **Tamamlanan Tahmini Puan:** 480 Puan ✅  
- **Dağılım:**  
  - HTML raporlama + modern UI: 150 puan  
  - Gemini & GPT entegrasyonu: 150 puan  
  - Yapay zekâ açıklama modülü: 100 puan  
  - Güvenlik & hasta geçmişi: 80 puan  

## Günlük Scrumlar
- WhatsApp + Google Meet  
- Chatbot ve HTML raporlama modülü canlı test edildi  

## Ekran Görüntüleri
[Ekran Görüntüleri Albümü](https://imgur.com/a/w0faUG7)

## Sprint Retrospektifi
- HTML raporlama güvenilir çıktı sağladı  
- Yapay zekâ entegrasyonu sistemi benzersiz kıldı  
- Risk analizleri görsel olarak daha anlaşılır hale geldi  
- Uygulama klinik kullanıma hazır hale getirildi  

---

## 📌 Genel Değerlendirme
Sprint 1’den Sprint 3’e kadar Perisentez; basit bir prototipten çıkıp **AI destekli açıklamalar, modern HTML raporlama ve güvenli hasta verisi yönetimi** ile klinik pratikte kullanılabilecek düzeyde bir **karar destek sistemi** haline gelmiştir. 🚀


## Lisans

Bu repo [Apache-2.0](LICENSE) ile lisanslıdır.
