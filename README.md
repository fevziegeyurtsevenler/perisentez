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
