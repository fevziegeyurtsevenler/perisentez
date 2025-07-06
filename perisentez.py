import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Prenatal Sendrom Risk Tahmini", layout="wide")
st.title("👶 PERİSENTEZ")

st.markdown("""
Perisentez'e Hoş Geldiniz! Bu uygulama, girdiğiniz prenatal ultrason bulguları ve serum verileri ışığında, olası genetik sendromların riskini **destekleyici bir araç olarak** değerlendirir.
**Önemli Not:** Perisentez, eğitim ve prototipleme amacıyla geliştirilmiş bir demo sürümüdür. Lütfen unutmayın ki tüm klinik tanı ve karar verme süreçleri, mutlaka uzman hekimler tarafından kapsamlı testler ve değerlendirmeler sonucunda yürütülmelidir.
""")

# --- Tıbbi Veriler ve Eşikler ---
# Sendromlara ait major yapısal anomaliler
sendrom_marker_verileri = {
    "Down (Trizomi 21)": [
        "Atriyoventriküler septal defekt (AV kanal)",
        "Duodenal atrezi (\"double-bubble\" işareti)",
        "Nazal kemik yokluğu",
        "Kısa uzun kemikler"
    ],
    "Edwards (Trizomi 18)": [
        "Omfalosel / ön abdominal duvar defekti",
        "Persistan \"clenched fist\" + rocker-bottom ayak postürü",
        "Kompleks kardiyak defektler (TOF, HLHS vb.)",
        "Mikrognati",
        "Koroid Pleksus Kisti"
    ],
    "Patau (Trizomi 13)": [
        "Alobar holoprozensefali (CNS orta-hat birleşme bozukluğu)",
        "Orta-hat yüz yarıkları (yarık damak-dudak) ± proboscis",
        "Postaksiyel polidaktili ± polikistik böbrek / büyük kardiyak defekt"
    ],
    "Turner (45,X)": [
        "Septalı dev kistik higroma",
        "Hidrops fetalis",
        "Sol kalp obstrüksiyonları – özellikle aort koarktasyonu"
    ],
    "DiGeorge (22q11.2 delesyonu)": [
        "Konotrunkal kalp defektleri (interrupted aortic arch tip B, truncus arteriosus, tetraloji vb.)",
        "Timus hipoplazisi/agenesisi (ultrasonda timus yokluğu)",
        "Sağ aortik ark veya vasküler ring anomalileri"
    ]
}

# Sayısal Değerler İçin Ortalama, SD ve Kritik Eşikler
# NT için haftalık ortalama ve SD (yaklaşık değerler, klinik tablodan yorumlandı)
nt_ortalama_sd = {
    10: {"ortalama": 1.0, "sd": 0.4},
    11: {"ortalama": 1.0, "sd": 0.4},
    12: {"ortalama": 1.2, "sd": 0.45},
    13: {"ortalama": 1.4, "sd": 0.5},
    14: {"ortalama": 1.5, "sd": 0.5} # 14. hafta için varsayımsal eklendi
}

# FL için genel bir ortalama ve SD (20. hafta örneği)
fl_ortalama_20w = 29.5
fl_sd_20w = 1.8

# βhCG ve PAPP-A MoM risk eşikleri
bhcg_dusuk_risk_esigi = 0.2
bhcg_yuksek_risk_esigi = 5.0
pappa_dusuk_risk_esigi = 0.5

# --- Kullanıcıdan Veri Al ---
st.sidebar.header("🧬 Prenatal Girdi Verileri")

# Gebelik Haftası
ga = st.sidebar.slider("Gebelik Haftası (GA)", 10, 40, 12, help="Ultrason muayenesinin yapıldığı gebelik haftası.")

# NT (Ense Kalınlığı)
nt_value = st.sidebar.number_input("NT (Ense Kalınlığı - mm)", min_value=0.0, value=1.5, step=0.1, help="Nukal translüsensi ölçümü. Kritik eşik ≥ 2.6 mm veya ≥ 3.0-3.5 mm'dir.")

# FL (Femur Uzunluğu)
fl_value = st.sidebar.number_input("FL (Femur Uzunluğu - mm)", min_value=0.0, value=30.0, step=0.1, help="Femur uzunluğu ölçümü. Z-skor ≤ -2 kritik eşiktir (ortalama -2xSD).")

# βhCG MoM
bhcg_value = st.sidebar.number_input("βhCG (MoM)", min_value=0.0, value=1.0, step=0.1, help="Serbest beta-hCG MoM değeri. <0.2 veya >5.0 artmış riske işaret edebilir.")

# PAPP-A MoM
pappa_value = st.sidebar.number_input("PAPP-A (MoM)", min_value=0.0, value=1.0, step=0.1, help="PAPP-A MoM değeri. <0.5 risk artışına işaret edebilir.")

st.sidebar.markdown("---")
st.sidebar.subheader("Önemli Yapısal Anomaliler (Hard Marker'lar)")
# Tüm olası bulguları dinamik olarak topla ve checkbox olarak göster
tum_hard_marker_bulgular = []
for sendrom, bulgular in sendrom_marker_verileri.items():
    tum_hard_marker_bulgular.extend(bulgular)
tum_hard_marker_bulgular = sorted(list(set(tum_hard_marker_bulgular))) # Tekrar edenleri kaldır ve sırala

secilen_hard_markerlar = []
for bulgu in tum_hard_marker_bulgular:
    if st.sidebar.checkbox(bulgu, value=False):
        secilen_hard_markerlar.append(bulgu)

# --- Risk Hesaplama (Kural Tabanlı) ---
st.subheader("📊 Tahmini Risk Değerlendirmesi")

# Her sendrom için risk puanı ve eşleşen bulgular
sendrom_riskleri = {}

# Sayısal değerlerin genel risk katkısı (sendrom spesifik olmayan)
nt_risk_genel = 0
if ga in nt_ortalama_sd:
    ortalama = nt_ortalama_sd[ga]["ortalama"]
    sd = nt_ortalama_sd[ga]["sd"]
    if sd > 0: # Sıfır SD'ye bölme hatasını önlemek için
        nt_z_skor = (nt_value - ortalama) / sd
        if nt_z_skor >= 2: # Z-skor 2 ve üzeri
            nt_risk_genel = 1 # Hafif risk
        if nt_z_skor >= 3: # Z-skor 3 ve üzeri (yaklaşık 3.0-3.5 mm kritik eşiğe denk gelir)
            nt_risk_genel = 2 # Yüksek risk
elif nt_value >= 2.6: # Genel kritik eşik (eğer gebelik haftası verisi yoksa veya eşleşmiyorsa)
    nt_risk_genel = 1
elif nt_value >= 3.0: # Daha yüksek genel kritik eşik
    nt_risk_genel = 2

fl_risk_genel = 0
# FL için Z-skor mantığı (20. hafta baz alınarak basitçe)
# Daha gelişmiş bir model için GA'ya göre FL ortalama/SD değerleri eklenebilir
if ga == 20: # Sadece 20. hafta için örnek olarak
    if fl_sd_20w > 0:
        fl_z_skor = (fl_value - fl_ortalama_20w) / fl_sd_20w
        if fl_z_skor <= -2: # Z-skor ≤ -2 kritik eşik
            fl_risk_genel = 2 # Yüksek risk

bhcg_risk_genel = 0
if bhcg_value < bhcg_dusuk_risk_esigi or bhcg_value > bhcg_yuksek_risk_esigi:
    bhcg_risk_genel = 2 # Yüksek risk

pappa_risk_genel = 0
if pappa_value < pappa_dusuk_risk_esigi:
    pappa_risk_genel = 2 # Yüksek risk

# Sendromların bulgularıyla eşleşme kontrolü
for sendrom_adi, sendrom_bulgulari in sendrom_marker_verileri.items():
    eslesen_bulgu_sayisi = 0
    eslesen_bulgular_listesi = []
    
    # Hard Marker eşleşmeleri
    for bulgu in secilen_hard_markerlar:
        if bulgu in sendrom_bulgulari:
            eslesen_bulgu_sayisi += 1
            eslesen_bulgular_listesi.append(bulgu)
    
    # Sayısal değerlerin sendromlara özgü risk katkısı
    sendrom_ozel_risk_puani = 0
    
    # Down Sendromu için sayısal marker değerlendirmesi
    if sendrom_adi == "Down (Trizomi 21)":
        if nt_risk_genel >= 1: # NT yüksekse Down riski artar
            sendrom_ozel_risk_puani += nt_risk_genel
            if nt_risk_genel == 1: eslesen_bulgular_listesi.append(f"NT (Ense Kalınlığı): {nt_value} mm (Yüksek)")
            elif nt_risk_genel == 2: eslesen_bulgular_listesi.append(f"NT (Ense Kalınlığı): {nt_value} mm (Çok Yüksek/Kritik)")
        if pappa_value < 0.5: # PAPP-A düşükse Down riski artar
            sendrom_ozel_risk_puani += 1
            eslesen_bulgular_listesi.append(f"PAPP-A (MoM): {pappa_value} (Düşük)")
        if bhcg_value > 2: # βhCG yüksekse Down riski artar (örnek eşik, literatürde >2 MoM kabul edilebilir)
            sendrom_ozel_risk_puani += 1
            eslesen_bulgular_listesi.append(f"βhCG (MoM): {bhcg_value} (Yüksek)")
        if "Kısa uzun kemikler" in secilen_hard_markerlar and fl_risk_genel >= 1: # FL kısalığı ile ilişkilendirilebilir
             sendrom_ozel_risk_puani += fl_risk_genel

    # Edwards Sendromu için sayısal marker değerlendirmesi
    elif sendrom_adi == "Edwards (Trizomi 18)":
        if nt_risk_genel >= 1: # NT yüksekse Edward riski de artabilir
            sendrom_ozel_risk_puani += nt_risk_genel
            if nt_risk_genel == 1: eslesen_bulgular_listesi.append(f"NT (Ense Kalınlığı): {nt_value} mm (Yüksek)")
            elif nt_risk_genel == 2: eslesen_bulgular_listesi.append(f"NT (Ense Kalınlığı): {nt_value} mm (Çok Yüksek/Kritik)")
        if pappa_value < 0.3: # PAPP-A çok düşükse Edward riski artar
            sendrom_ozel_risk_puani += 1
            eslesen_bulgular_listesi.append(f"PAPP-A (MoM): {pappa_value} (Çok Düşük)")
        if bhcg_value < 0.3: # βhCG çok düşükse Edward riski artar
            sendrom_ozel_risk_puani += 1
            eslesen_bulgular_listesi.append(f"βhCG (MoM): {bhcg_value} (Çok Düşük)")
        if fl_risk_genel >= 1: # FL kısalığı Edward ile ilişkilidir
            sendrom_ozel_risk_puani += fl_risk_genel
            eslesen_bulgular_listesi.append(f"FL (Femur Uzunluğu): {fl_value} mm (Kısa)")


    # Patau Sendromu için sayısal marker değerlendirmesi
    elif sendrom_adi == "Patau (Trizomi 13)":
        if nt_risk_genel >= 1: # NT yüksekse Patau riski de artabilir
            sendrom_ozel_risk_puani += nt_risk_genel
            if nt_risk_genel == 1: eslesen_bulgular_listesi.append(f"NT (Ense Kalınlığı): {nt_value} mm (Yüksek)")
            elif nt_risk_genel == 2: eslesen_bulgular_listesi.append(f"NT (Ense Kalınlığı): {nt_value} mm (Çok Yüksek/Kritik)")
        if pappa_value < 0.3: # PAPP-A çok düşükse Patau riski artar
            sendrom_ozel_risk_puani += 1
            eslesen_bulgular_listesi.append(f"PAPP-A (MoM): {pappa_value} (Çok Düşük)")
        if bhcg_value < 0.3: # βhCG çok düşükse Patau riski artar
            sendrom_ozel_risk_puani += 1
            eslesen_bulgular_listesi.append(f"βhCG (MoM): {bhcg_value} (Çok Düşük)")

    # Turner Sendromu için sayısal marker değerlendirmesi
    elif sendrom_adi == "Turner (45,X)":
        if nt_risk_genel >= 1: # NT yüksekse Turner riski de artabilir
            sendrom_ozel_risk_puani += nt_risk_genel
            if nt_risk_genel == 1: eslesen_bulgular_listesi.append(f"NT (Ense Kalınlığı): {nt_value} mm (Yüksek)")
            elif nt_risk_genel == 2: eslesen_bulgular_listesi.append(f"NT (Ense Kalınlığı): {nt_value} mm (Çok Yüksek/Kritik)")

    # Toplam puan (hard marker + sayısal verinin sendrom özel katkısı)
    # Basit bir puanlama: Her eşleşen hard marker 1 puan, sayısal risk puanı direkt ekleniyor
    toplam_puan = eslesen_bulgu_sayisi + sendrom_ozel_risk_puani

    # Sendromun tüm major marker'larına göre eşleşme yüzdesi
    if len(sendrom_bulgulari) > 0:
        # Puanlama sistemini sendromun orijinal hard marker sayısı ve sayısal risk katkısına göre ayarlayalım
        # Her hard marker 1 puan, sayısal risk katkısı max 2 puan (nt_risk_genel max 2, diğerleri 1)
        # Daha karmaşık bir puanlama/AI modeli bu kısımda devreye girecek
        maksimum_olasi_puan = len(sendrom_bulgulari) + 3 # Genel bir maks puan, her sendrom için özelleştirilebilir
        
        if maksimum_olasi_puan == 0: maksimum_olasi_puan = 1 # Sıfıra bölme hatasını engelle
        
        yuzde_eslesme = (toplam_puan / maksimum_olasi_puan) * 100
        
        # Sadece eşleşme olan sendromları veya belirli bir eşiğin üzerindekileri listele
        if yuzde_eslesme > 0 or len(eslesen_bulgular_listesi) > 0:
            sendrom_riskleri[sendrom_adi] = {
                "puan": toplam_puan,
                "yuzde": min(yuzde_eslesme, 100), # Yüzdeyi 100 ile sınırlayalım
                "eslesen_bulgular": list(set(eslesen_bulgular_listesi)) # Tekrar edenleri kaldır
            }

# Sonuçları yüzdeye göre azalan sırada sırala
sirali_sendromlar = sorted(sendrom_riskleri.items(), key=lambda item: item[1]["yuzde"], reverse=True)

if sirali_sendromlar:
    st.markdown("### Olası Sendromlar:")
    for sendrom_adi, data in sirali_sendromlar:
        st.write(f"#### {sendrom_adi}")
        st.progress(data['yuzde'] / 100)
        st.info(f"**Tahmini Eşleşme Oranı:** %{data['yuzde']:.2f}")
        if data['eslesen_bulgular']:
            st.markdown(f"**Girilen ve {sendrom_adi} ile İlişkili Bulgular:**")
            for bulgu in data['eslesen_bulgular']:
                st.write(f"- {bulgu}")
        else:
            st.write("Girilen bulgular arasında bu sendromla doğrudan ilişkili spesifik bulgu bulunamadı.")
        st.markdown("---") # Her sendromdan sonra ayırıcı çizgi ekleniyor
else:
    st.warning("Girilen bulgularla eşleşen önemli bir genetik sendrom bulunamadı.")
    st.markdown("""
    * Farklı bulgular denediğinizden veya girdiğiniz değerleri kontrol ettiğinizden emin olun.
    * Unutmayın, bu prototip sadece sınırlı sayıda sendromu ve kural tabanlı bir risk değerlendirme mantığını kullanmaktadır.
    * Gerçek klinik durumlar ve kesin tanı için daima uzman bir hekime danışmanız önemle tavsiye edilir.
    """)

# --- Açıklama ve Notlar ---
st.markdown("---")
st.markdown("""
### Perisentez: Derinlemesine Bakış

* **Kural Tabanlı Yaklaşım:** Perisentez, genel kabul görmüş prenatal bulgulara ve sayısal eşiklere dayalı, basit ancak etkili bir kural setini kullanır. Bu yaklaşım, hızlı ve anlaşılır bir ön değerlendirme sunmayı amaçlar.
* **Yapay Zeka ve Gelecek Vizyonu:** Gerçek yapay zeka modelleri, çok daha geniş veri kümeleri, karmaşık istatistiksel analizler, gelişmiş makine öğrenimi algoritmaları ve derin klinik korelasyonlar gerektirir. Perisentez'in bu prototip versiyonu, gelecekte entegre etmeyi hedeflediğimiz yapay zeka destekli bir klinik karar destek sisteminin temel prensiplerini ve potansiyelini gözler önüne sermektedir.
* **Kullanım Amacı ve Sınırlamalar:** Bu demo sürümü, sadece eğitim ve demonstrasyon amaçlıdır. **Kesin tanı, tedavi planlaması veya tıbbi tavsiye yerine geçmez.** Tüm tıbbi kararlar, yetkili sağlık profesyonelleri tarafından verilmelidir.
* **Sürekli Gelişim:** Perisentez sürekli olarak geliştirilmektedir. Gelecekte yeni sendromlar, ek bulgular ve daha gelişmiş algoritmalarla güncellemeler yapılacaktır. Geri bildirimleriniz projenin gelişimine büyük katkı sağlamaktadır.
""")