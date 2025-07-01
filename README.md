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

## Ürün Açıklaması
Prenatal Diagnosis Assistant, prenatal (doğum öncesi) dönemde ultrason bulgularına göre genetik sendrom tahmini yaparak, uzman hekimlere karar desteği sunan bir yapay zekâ tabanlı asistan sistemidir.

Uygulama, hekimin seçtiği fetal bulgularla veri tabanındaki sendromlar arasında benzerlik eşleştirmesi yaparak, olası sendromları sıralar. Bu sayede doğru tanıya daha hızlı ulaşılmasına katkı sağlar. Sistem aynı zamanda bulguların açıklamalarını sunarak, klinik süreci bilgi açısından da destekler.
## Ürün Özellikleri
- Kullanıcı arayüzünden fetal bulguların girişini sağlama

- Gelişmiş algoritmalarla benzer sendrom eşleştirmesi yapma

- En yüksek benzerliğe sahip ilk 3 sendromun kullanıcıya önerilmesi

- Her sendromun ICD kodu, fenotip tanımı ve açıklamalarının sunulması

- Otomatik doldurma (autocomplete) özellikli bulgu arama çubuğu

- Örnek hasta senaryosu ile model test imkanı

- Hekim destekli, klinik kullanım odaklı tasarım

## Hedef Kitle
- Perinatoloji uzmanları

- Kadın doğum doktorları

- Tıp fakültesi öğrencileri (özellikle prenatal tanı çalışanlar)

- Genetik danışmanlar

- Yapay zekâ destekli tıbbi sistemler geliştirmek isteyen araştırmacılar
## Product Backlog URL
[Trello Backlog](https://trello.com/b/U1T5wQXG/prenatal-diagnosis-ai)
## User Story
Senaryo: Deneyimli bir perinatoloji uzmanı olan Dr. Şeyda, detaylı ikinci düzey ultrason muayenesi sırasında fetüste birkaç sıra dışı bulgu tespit eder. Örneğin, fetüsün burun kemiğinin oluşmadığını, kalpte dört odacık görüntüsünde bir anormallik olduğunu ve bacak kemiklerinin gebelik haftasına göre kısa kaldığını gözlemler. Bu bulgular bir dizi genetik sendromu akla getirebilir; ancak her sendromun belirtilerini tek tek hatırlamak güçtür. Dr. Şeyda, hastanede kullanıma yeni sunulan yapay zekâ destekli prenatal tanı uygulamasına giriş yapar:
1.⁠ ⁠Veri Girişi: Uygulamanın arama çubuğu şeklindeki akıllı giriş alanına bulguları yazmaya başlar. “Burun kemiği yokluğu” yazdığında sistem otomatik olarak ilgili tıbbi terimi tanıyıp önerir. Ardından “kısa femur” ve “kalp septal defekti” gibi bulguları da ekler. Girdiği her bulgu, uygulama tarafından doğrulanır ve standart terminolojiye dönüştürülür (ör. “nazal kemik yokluğu” gibi), böylece veri tutarlılığı sağlanır.

2.⁠ ⁠Analiz ve Hesaplama: Dr. Şeyda “Analiz Et” butonuna bastığında, uygulamanın arka plandaki yapay zekâ modeli saniyeler içinde girilen belirtileri işler. Model, geniş bir tıbbi veri tabanındaki genetik sendromları ve onların tipik bulgularını tarayarak, Dr. Şeyda’nın girdiği kombinasyona en çok uyan sendromları tespit eder.

3.⁠ ⁠Karar Desteği Çıktısı: Ekranda olası sendromların bir listesi belirir. Örneğin, Down Sendromu (Trizomi 21) için %85 eşleşme olasılığı, DiGeorge Sendromu (22q11 delesyonu) için %60 olasılık, ve birkaç daha nadir sendrom için daha düşük yüzdeler gösterilir. Uygulama, her sendromun Dr. Şeyda’nın girdiği bulgularla hangi yönlerden eşleştiğini açıklayan kısa notlar da sunar (örn. Down sendromunda nazal kemik yokluğu ve kardiyak defekt sık görülür). Bu sayede Dr. Şeyda, listelenen sendrom adaylarının hangi bulgular nedeniyle öne çıktığını anında kavrar.

4.⁠ ⁠İleri Adımlar: Dr. Şeyda, yapay zekânın sunduğu bu ön tanı destek listesini kendi klinik deneyimiyle birleştirerek hastaya en uygun danışmanlığı verir. Örneğin yüksek olasılıklı Down sendromu ihtimaline karşı amniyosentez veya NIPT gibi ileri genetik tetkikleri önerir. Daha nadir görülen ancak listede çıkan bir sendrom varsa, o sendromla ilişkili ekstra taramaları planlar veya genetik danışmanlık alır. Uygulama, Dr. Şeyda’ya unuttuğu veya nadir rastlanan bir sendromu hatırlatarak kritik bir katkı sunmuştur.
Bu kullanıcı senaryosunda görüldüğü gibi sistemimiz, kullanım kolaylığı, hızlı geri dönüş ve güvenilir öneriler ile klinik akışı bozmadan doktorun karar alma sürecine entegre olur. Sonuç olarak, anne karnındaki bebeğin durumu hakkında daha kapsamlı bir öngörü elde edilmesini ve doğru yönlendirmelerin yapılmasını sağlar.
# Sprint 1
