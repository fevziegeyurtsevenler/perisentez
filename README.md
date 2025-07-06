## Takım İsmi
**Timpossible**

## Takım Elemanları

| Name                | Title          | Social                                                           |
| :------------------ | :------------- | :--------------------------------------------------------------- |
| Feyza Hilal Şahin | Product Owner   | [LinkedIn](https://tr.linkedin.com/in/feyza-hilal-%C5%9Fahin-153989210)     |
| Fevzi Ege Yurtsevenler    | Scrum Master  | [LinkedIn](https://www.linkedin.com/in/fevziege/)         |
| Sena Açıkgöz      | Developer      | [LinkedIn](https://www.linkedin.com/in/sena-açıkgöz00)          |
| Semanur Büdün      | Developer      | [LinkedIn](https://www.linkedin.com/in/semanur-budun)          |
| Tarık Anafarta      | Developer      | [LinkedIn](https://www.linkedin.com/in/tarik-anafarta)          |

## Ürün İsmi
Perisentez

## Ürün Açıklaması
Prenatal (doğum öncesi) dönemde ultrason bulgularına göre genetik sendrom tahmini yaparak, uzman hekimlere karar desteği sunan bir yapay zekâ tabanlı asistan sistemidir.

Uygulama, hekimin seçtiği fetal bulgularla veri tabanındaki sendromlar arasında benzerlik eşleştirmesi yaparak, olası sendromları sıralar. Bu sayede doğru tanıya daha hızlı ulaşılmasına katkı sağlar. Sistem aynı zamanda bulguların açıklamalarını sunarak, klinik süreci bilgi açısından da destekler.
## Ürün Özellikleri
Perisentez, prenatal dönemde ultrason bulgularına göre genetik sendrom tahmini yaparak, uzman hekimlere karar desteği sunan yapay zekâ tabanlı bir asistan sistemidir.

* **Prenatal Ultrason ve Serum Veri Girişi:**
    * Kullanıcılar, gebelik haftası, ense kalınlığı (NT), femur uzunluğu (FL), serbest beta-hCG MoM ve PAPP-A MoM değerleri gibi sayısal prenatal verileri sisteme girebilir.
    * Önemli yapısal anomaliler (hard marker'lar) listeden seçilebilir (örneğin, Atriyoventriküler septal defekt, Omfalosel, Holoprozensefali).

* **Kural Tabanlı Sendrom Risk Değerlendirmesi:**
    * Girilen sayısal değerler ve seçilen yapısal bulgulara dayanarak, önceden tanımlanmış tıbbi kurallar ve eşikler kullanılarak olası genetik sendromların riski hesaplanır.
    * Sistem, her bir sendrom için sayısal ve yapısal bulguların eşleşme derecesine göre bir "tahmini eşleşme oranı" sunar.

* **Potansiyel Sendromların Sıralı Listelenmesi:**
    * Hesaplanan eşleşme oranına göre en olası sendromlar azalan sırada listelenir.
    * Her bir sendrom için eşleşen spesifik bulgular açıkça belirtilir, bu da hekime kararı destekleyici bilgi sağlar.

* **Açıklayıcı ve Uyarıcı Bilgilendirme:**
    * Uygulamanın eğitim amaçlı bir prototip olduğu ve klinik karar alma süreçlerinin yalnızca uzman doktorlar tarafından yürütülmesi gerektiği vurgulanır.
    * Sistemin kural tabanlı yapısı ve gerçek yapay zeka modellerinin karmaşıklığı hakkında genel bir açıklama sunulur.

## Hedef Kitle
- Perinatoloji uzmanları

- Kadın doğum doktorları

- Tıp fakültesi öğrencileri (özellikle prenatal tanı çalışanlar)

- Genetik danışmanlar

- Yapay zekâ destekli tıbbi sistemler geliştirmek isteyen araştırmacılar
## Product Backlog URL
[Trello Backlog](https://trello.com/b/U1T5wQXG/prenatal-diagnosis-ai)
## User Story
Kullanıcı Tipi: Perinatoloji Uzmanı (Dr. Şeyda)

User Story:

“Bir perinatoloji uzmanı olarak, detaylı ultrason muayenesinde tespit ettiğim fetal bulguları sisteme girerek bu bulgularla en çok eşleşen genetik sendromların listesini görmek istiyorum. Böylece olası tanıları daha hızlı değerlendirebilir ve hastaya en uygun ileri test ve yönlendirmeyi yapabilirim.”

Kabul Kriterleri:

Kullanıcı, arama çubuğuna bulguları yazabilir ve sistem otomatik tamamlama önerileri sunar

Girilen her bulgu sistem tarafından doğrulanarak standart tıbbi terimlere dönüştürülür

"Analiz Et" butonuna basıldığında sistem ilk 3 olası sendromu benzerlik oranları ile sıralar

Her sendrom için ICD kodu, fenotip tanımı ve açıklayıcı bilgiler gösterilir

Listeleme sonucunda, her sendromun hangi bulgularla eşleştiği ayrı ayrı belirtilir

Hekim bu bilgilerle daha bilinçli yönlendirmeler yapabilir (ör. NIPT, amniyosentez)
# Sprint 1

### Genel Kararlar ve Kullanılan Araçlar

* **UI Tasarımları:** Sprint 1'de ayrı bir UI tasarım aracı kullanılmamıştır. Kullanıcı arayüzü, doğrudan Streamlit kütüphanesi kullanılarak (`sendrom.py` dosyası içerisinde) kodlanmıştır.
* **Proje Yönetimi:** Proje yönetimi ve görev takibi için **Trello** platformu aktif olarak kullanılmıştır.
* **Günlük Scrum Toplantıları:** Takım üyelerinin uygunluğuna göre **WhatsApp** grup sohbetleri ve **Google Meet** video konferansları üzerinden günlük scrum toplantıları gerçekleştirilmiştir.
* **Uygulama Teması:** Uygulamanın görsel tasarımı için kod içinde belirlendiği üzere **koyu (dark) tema** tercih edilmiştir.
* **Tasarım ve Uygulama Dili:** Uygulamanın arayüz metinleri ve çıktıları, hedef kitlenin ihtiyaçları doğrultusunda **Türkçe** olarak tasarlanmış ve geliştirilmiştir.

---

### Beklenen Puan Tamamlama

* **Sprint 1 Hedefi:** 300 Puan
* **Puan Tamamlama Mantığı:**
    * Projenin genel tamamlanma hedefi 1200 puan olarak belirlenmiştir.
    * Sprint 1, Perisentez uygulamasının **Minimum Uygulanabilir Ürün (MVP)** aşamasını oluşturduğu için 300 puanlık bir ağırlık verilmiştir.
    * Bu sprintin ana odak noktaları; projenin fikir aşamasını netleştirmek, ürün özelliklerini detaylandırmak ve temel fonksiyonelliği içeren **çalışır bir prototip (`sendrom.py`)** geliştirmek olmuştur.
    * Kullanıcı arayüzünün Streamlit ile kodlanması, temel veri giriş mekanizmalarının oluşturulması, kural tabanlı eşleştirme algoritmasının uygulanması ve çıktıların gösterilmesi gibi görevlerin başarıyla tamamlanmasıyla 300 puanlık hedefe ulaşılmıştır.
    * Toplam 1200 puanlık genel hedefin geri kalan dağılımı şu şekildedir: İkinci sprintte kod yazımına ve API entegrasyonlarına odaklanılacağı için 450 puan, üçüncü sprintte ise kalan görevlerin tamamlanması ve entegrasyon çalışmalarına ayrılacağı için yine 450 puan hedeflenmiştir.

---

### Günlük Scrumlar

* **Sprint 1 Günlük Scrum Özeti:** Günlük scrum toplantıları, takım üyelerinin mevcut ilerlemelerini paylaşmaları, karşılaşılan engelleri tartışmaları ve bir sonraki günün görevlerini belirlemeleri amacıyla düzenli olarak yapılmıştır. Hızlı iletişim ve görev takibi için WhatsApp grubu kullanılırken, daha detaylı tartışmalar ve ekran paylaşımı gerektiren konular için Google Meet tercih edilmiştir.

---


### Sprint Değerlendirmesi (Sprint Review)

* **Tamamlanan İşler:**
    * **Fetal Bulguların Arayüzden Girişi:** Kullanıcı arayüzünde, gebelik haftası, NT, FL, beta-hCG MoM, PAPP-A MoM gibi sayısal prenatal değerler ve önemli yapısal anomaliler (hard marker'lar) için seçim kutuları (checkbox'lar) aracılığıyla veri giriş alanları başarıyla oluşturulmuştur.
    * **Kural Tabanlı Sendrom Risk Değerlendirmesi:** Girilen sayısal veriler ve seçilen yapısal bulgulara dayanarak, `sendrom.py` modülü içinde tanımlanan tıbbi kurallar ve eşikler kullanılarak olası genetik sendromların riski hesaplanmış ve bu mantık uygulamaya entegre edilmiştir. Her sendrom için "tahmini eşleşme oranı" sunulmaktadır.
    * **Potansiyel Sendromların Sıralı Listelenmesi:** Hesaplanan eşleşme oranına göre en olası sendromlar azalan sırada listelenmekte ve her bir sendrom için ilişkili girilen bulgular açıkça belirtilerek hekime karar destekleyici bilgi sağlanmaktadır.
    * **Açıklayıcı ve Uyarıcı Bilgilendirme:** Uygulamanın eğitim amaçlı bir prototip olduğu ve klinik karar verme sürecinin yalnızca uzman doktorlar tarafından yürütülmesi gerektiği vurgulayan uyarı ve açıklamalar arayüze entegre edilmiştir.
* **Karşılaşılan Zorluklar ve Çıkarımlar:**
    * Uygulamanın "Yapay Zeka Destekli Asistan Sistem" tanımını mevcut kural tabanlı MVP yapısıyla nasıl dengeleyeceğimiz üzerine ekip içi tartışmalar yaşanmıştır. İlk aşamada güçlü bir kural seti ile ilerlemenin, daha sonra gerçek AI modellerini entegre etmek için sağlam bir temel oluşturacağı kararlaştırılmıştır.
    * Perisentez'in temel felsefesi olan "klinik karara destek" misyonu üzerinde durularak, uygulamanın bir tanı koyucu olmaktan ziyade, hekimlere bilgi ve yönlendirme sunan bir asistan görevi görmesi gerektiği vurgulanmıştır.
    * İlk hafta, kullanıcı hikayesi ve kabul kriterleri doğrultusunda veri giriş arayüzünün ve temel kural setinin işleyişi detaylıca planlanmıştır. İkinci hafta ise Streamlit arayüzünün aktif olarak kodlanması ve risk hesaplama mantığının entegrasyonu başarıyla gerçekleştirilmiştir.
* **Genel Değerlendirme:** Sprint 1, Perisentez projesinin temel işlevsel iskeletini oluşturarak, fikrin çalışır bir prototipe dönüşümü açısından oldukça verimli ve başarılı bir süreç olmuştur.

* **Sprint Değerlendirmesi Katılımcıları:**
    * Feyza Hilal Şahin (Product Owner)
    * Fevzi Ege Yurtsevenler (Scrum Master)
    * Sena Açıkgöz (Developer)
    * Semanur Büdün (Developer)
    * Tarık Anafarta (Developer)
  
---

### Ekran Görüntüleri

Uygulama ve daily scrumlar ile ilgili ekran görüntüleri:

[Ekran Görüntüleri Albümü](https://imgur.com/a/Bc1tRcg)


---

### Sprint Retrospektifi

* **İkinci Sprint için Kararlar ve İyileştirmeler:**
    * Daha kapsamlı veri yönetimi ve gelecekteki olası yapay zeka modelleri için **Firebase gibi bir backend çözümünün** araştırılmasına ve entegre edilmesine öncelik verilmesine karar verildi.
    * Uygulamanın **logosunun ve genel marka kimliğinin** kesinleştirilmesi planlandı.
    * İkinci sprintte tüm takım üyelerinin **kod geliştirme süreçlerine daha aktif ve eş zamanlı olarak katılmasına** karar verildi.
    * Yapay zeka eklentisi için uygulamaya uygun, **ücretsiz veya uygun maliyetli API'lerin araştırılması** yapılacak (özellikle daha gelişmiş bulgu eşleştirme veya açıklayıcı AI modelleri için).
    * Klinik raporların daha kullanıcı dostu olması ve hekimler arası paylaşılabilirliğini artırmak amacıyla **PDF formatında risk raporu dışa aktarma** özelliğinin araştırılmasına karar verildi.
    * Sendromlara ilişkin **ICD kodları** ve **daha detaylı fenotip tanımlarının** (her sendrom için açıklayıcı bilgiler) veri tabanına eklenmesi ve arayüzde gösterilmesi üzerine çalışılacak.
    * Gelecek sprintlerde, sayısal bulguların gebelik haftasına göre daha dinamik ve yaşa özgü değerlendirilmesi gibi algoritmik iyileştirmelerin araştırılmasına karar verildi.
