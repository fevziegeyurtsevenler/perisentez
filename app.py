import streamlit as st
import pandas as pd
import joblib
import uuid
import os
import hashlib
import sqlite3
import matplotlib.pyplot as plt
from fpdf import FPDF 
from datetime import datetime
import requests
import json

def sanitize_text(text):
    """Türkçe karakterleri ve tüm non-ASCII karakterleri ASCII karakterlere dönüştürür"""
    if text is None:
        return ""
    
    result = str(text)
    
    # Türkçe karakterleri değiştir
    replacements = {
        'ı': 'i', 'İ': 'I', 'ş': 's', 'Ş': 'S',
        'ç': 'c', 'Ç': 'C', 'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O',
        'â': 'a', 'Â': 'A', 'î': 'i', 'Î': 'I',
        'û': 'u', 'Û': 'U', 'ô': 'o', 'Ô': 'O'
    }
    
    for turkish, english in replacements.items():
        result = result.replace(turkish, english)
    
    # Tüm non-ASCII karakterleri kaldır veya değiştir
    try:
        # ASCII olmayan karakterleri kaldır
        result = result.encode('ascii', 'ignore').decode('ascii')
    except:
        # Son çare: sadece ASCII karakterleri tut
        result = ''.join(char for char in result if ord(char) < 128)
    
    return result

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Sadece ASCII karakterler kullanacağız
        self.set_font("Arial", '', 12)

    def chapter_title(self, title):
        self.set_font("Arial", 'B', 14)
        # Türkçe karakterleri temizle
        clean_title = sanitize_text(title)
        self.multi_cell(0, 10, txt=clean_title, align='C')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Arial", '', 12)
        # Türkçe karakterleri temizle
        clean_body = sanitize_text(body)
        self.multi_cell(0, 8, txt=clean_body)
        self.ln()

def generate_explanation(values, predicted_syndrome):
    comments = []

    if values.get("NT (Ense kalınlığı)", 0) > 3.5:
        comments.append(f"Ense kalinligi {values['NT (Ense kalınlığı)']} mm olarak olculmus, bu deger 3.5 mm uzeri olup noral tup defekti veya trizomilerle iliskili olabilir.")
    if values.get("PAPP-A", 1) < 0.5:
        comments.append(f"PAPP-A seviyesi {values['PAPP-A']} MoM ile dusuktur; bu durum Down sendromu riskini artirabilir.")
    if values.get("β-hCG", 0) > 2.0:
        comments.append(f"beta-hCG degeri {values['β-hCG']} MoM ile normalin uzerindedir, bu da trizomi 21 (Down) ile uyumlu olabilir.")
    if values.get("FL (Femur uzunluğu)", 1000) < 15:
        comments.append(f"Femur uzunlugu {values['FL (Femur uzunluğu)']} mm olarak olculmus ve kisa olmasi kemik gelisim bozukluklarina isaret edebilir.")

    if comments:
        explanation = "Yorum: " + " ".join(comments)
    else:
        explanation = "Belirgin bir risk faktoru tespit edilmedi veya girilen verilerle dogrudan spesifik bir sendromla iliskilendirilebilecek yeterli bulguya ulasilamadi. Yapay zeka genel verilerle degerlendirme yapmistir."
    return explanation

# Chatbot fonksiyonları
def call_gemini_api(prompt, api_key):
    """Google Gemini API çağrısı"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Hatası: {response.status_code}"
    except Exception as e:
        return f"Hata: {str(e)}"

def call_openai_api(prompt, api_key):
    """OpenAI GPT API çağrısı"""
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Hatası: {response.status_code}"
    except Exception as e:
        return f"Hata: {str(e)}"

def chatbot_interface():
    """Chatbot arayüzü"""
    st.markdown("## 🤖 AI Danışman Chatbot")
    
    # API ayarları
    api_provider = st.selectbox("AI Sağlayıcısı Seçin:", ["Google Gemini", "OpenAI GPT"])
    api_key = st.text_input("API Anahtarı:", type="password", help="API anahtarınızı girin")
    
    if not api_key:
        st.warning("Lütfen API anahtarınızı girin.")
        st.info("📝 **API Anahtarı Nasıl Alınır:**\n\n"
                "**Google Gemini:** https://makersuite.google.com/app/apikey\n\n"
                "**OpenAI:** https://platform.openai.com/api-keys")
        return
    
    # Chat geçmişi
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Soru giriş alanı
    user_question = st.text_area("Sorunuzu yazın:", height=100, 
                                placeholder="Örn: Down sendromu hakkında bilgi verir misiniz?")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📨 Gönder", use_container_width=True):
            if user_question.strip():
                # Medikal kontekst ekleme
                context = """Sen bir tıbbi danışman asistanısın. Perinatology, genetik sendromlar, 
                prenatal tanı ve perisentez konularında uzmanlaşmış durumdasın. 
                Verdiğin bilgiler sadece eğitim amaçlıdır ve kesin tanı için doktora başvurulması gerektiğini belirt."""
                
                full_prompt = f"{context}\n\nSoru: {user_question}"
                
                with st.spinner("AI yanıt oluşturuyor..."):
                    if api_provider == "Google Gemini":
                        response = call_gemini_api(full_prompt, api_key)
                    else:
                        response = call_openai_api(full_prompt, api_key)
                
                # Chat geçmişine ekleme
                st.session_state.chat_history.append({"user": user_question, "ai": response})
                st.rerun()
    
    with col2:
        if st.button("🗑️ Geçmişi Temizle", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Chat geçmişini gösterme
    if st.session_state.chat_history:
        st.markdown("### 💬 Sohbet Geçmişi")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Son 5 mesaj
            with st.expander(f"Soru {len(st.session_state.chat_history)-i}: {chat['user'][:50]}..."):
                st.markdown(f"**👤 Siz:** {chat['user']}")
                st.markdown(f"**🤖 AI:** {chat['ai']}")

st.set_page_config(page_title="Perisentez", page_icon="🧬", layout="wide")

DB_PATH = "perisentez.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
    c.execute("""CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        patient_name TEXT,
        prediction TEXT,
        probability TEXT,
        date TEXT,
        pdf_file TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, pw_hash):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, pw_hash))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def validate_login(username, pw_hash):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, pw_hash))
    result = c.fetchone()
    conn.close()
    return result

def save_patient(username, name, pred, prob, pdf_file):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Verileri temizle ve güvenli hale getir
        clean_name = sanitize_text(str(name))
        clean_pred = sanitize_text(str(pred))
        clean_prob = f"{float(prob):.1f}"
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        c.execute("INSERT INTO patients (username, patient_name, prediction, probability, date, pdf_file) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, clean_name, clean_pred, clean_prob, current_date, pdf_file))
        conn.commit()
        success = True
        print(f"Hasta kaydedildi: {clean_name}")  # Debug için
    except Exception as e:
        print(f"Hasta kaydedilirken hata: {e}")  # Debug için
        success = False
    finally:
        conn.close()
    return success

def load_patients(username, search=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        if search:
            c.execute("SELECT * FROM patients WHERE username = ? AND LOWER(patient_name) LIKE ? ORDER BY date DESC", 
                     (username, f"%{search.lower()}%"))
        else:
            c.execute("SELECT * FROM patients WHERE username = ? ORDER BY date DESC", (username,))
        rows = c.fetchall()
    except Exception as e:
        st.error(f"Hasta kayıtları yüklenirken hata: {e}")
        rows = []
    finally:
        conn.close()
    return rows

def delete_patient(pid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # PDF dosyasını da sil
        c.execute("SELECT pdf_file FROM patients WHERE id = ?", (pid,))
        result = c.fetchone()
        if result and result[0] and os.path.exists(result[0]):
            os.remove(result[0])
        
        c.execute("DELETE FROM patients WHERE id = ?", (pid,))
        conn.commit()
        success = True
    except Exception as e:
        st.error(f"Hasta silinirken hata: {e}")
        success = False
    finally:
        conn.close()
    return success

def generate_pdf(patient_name, result_class, result_prob, df_probs, doktor, explanation=None):
    try:
        pdf = PDF()
        pdf.add_page()
        
        # Başlık
        title = "Perisentez Tahmin Raporu"
        pdf.chapter_title(title)
        
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        
        # Hasta bilgileri - Tüm metinleri temizle
        clean_patient_name = sanitize_text(str(patient_name))
        clean_result_class = sanitize_text(str(result_class))
        clean_doktor = sanitize_text(str(doktor))
        
        # Güvenli metin oluşturma
        patient_line = f"Hasta Adi: {clean_patient_name}"
        result_line = f"Tahmin Edilen Sendrom: {clean_result_class} ({result_prob:.1f}%)"
        doctor_line = f"Doktor: {clean_doktor}"
        date_line = f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Her satırı ayrı ayrı ekle
        pdf.cell(200, 10, txt=patient_line, ln=True)
        pdf.cell(200, 10, txt=result_line, ln=True)
        pdf.cell(200, 10, txt=doctor_line, ln=True)
        pdf.cell(200, 10, txt=date_line, ln=True)
        
        pdf.ln(5)
        pdf.cell(200, 10, txt="Tum Olasiliklar:", ln=True)
        
        # Açıklama ekle
        if explanation:
            pdf.ln(5)
            # Açıklamayı temizle ve sadeleştir
            clean_explanation = sanitize_text(str(explanation))
            # Uzun metinleri böl
            if len(clean_explanation) > 200:
                clean_explanation = clean_explanation[:200] + "..."
            
            try:
                pdf.multi_cell(0, 8, clean_explanation)
            except:
                # Eğer hala sorun varsa basit bir metin yaz
                pdf.multi_cell(0, 8, "Analiz yorumu mevcuttur.")
        
        pdf.ln(5)
        
        # Olasılık tablosu
        for _, row in df_probs.iterrows():
            try:
                clean_syndrome = sanitize_text(str(row['Sendrom']))
                probability_value = float(row['Olasılık (%)'])
                line_text = f"{clean_syndrome}: {probability_value:.1f}%"
                pdf.cell(200, 10, txt=line_text, ln=True)
            except Exception as e:
                # Eğer bir satırda sorun varsa atla
                continue
        
        pdf.ln(10)
        disclaimer = "Bu rapor on tani amaclidir. Kesin tani icin genetik danismanlık onerilir."
        pdf.multi_cell(0, 10, disclaimer)
        
        # Dosya adını güvenli hale getir
        safe_patient_name = sanitize_text(str(patient_name)).replace(' ', '_')
        # Dosya adında da sorun çıkmasın diye sadece alfanumerik karakterler
        safe_patient_name = ''.join(c for c in safe_patient_name if c.isalnum() or c in '_-')
        if not safe_patient_name:
            safe_patient_name = "hasta"
        
        fname = f"rapor_{safe_patient_name}_{uuid.uuid4().hex[:4]}.pdf"
        
        # PDF'i kaydet
        pdf.output(fname)
        
        # Dosyanın gerçekten oluştuğunu kontrol et
        if os.path.exists(fname):
            return fname
        else:
            return None
        
    except Exception as e:
        print(f"PDF oluşturma hatası: {e}")  # Debug için
        return None

def login_screen():
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="color: #4A7C59;">🧬 Perisentez Tahmin Sistemi</h1>
            <p style="font-size: 1.2rem; color: #666;">Prenatal Genetik Analiz Platformu</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Logo kodu kaldırıldı
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Doktor Giriş Paneli")
        with st.form("login_form"):
            username = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adınızı girin")
            password = st.text_input("🔒 Şifre", type="password", placeholder="Şifrenizi girin")
            login_btn = st.form_submit_button("🚀 Giriş Yap", use_container_width=True)
            
            if login_btn:
                if validate_login(username, hash_password(password)):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                    st.rerun()
                else:
                    st.error("❌ Hatalı kullanıcı adı veya şifre!")

def register_screen():
    st.markdown("### 👤 Yeni Hesap Oluştur")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("register_form"):
            username = st.text_input("👤 Kullanıcı Adı", placeholder="Benzersiz kullanıcı adı seçin")
            password = st.text_input("🔒 Şifre", type="password", placeholder="Güçlü bir şifre oluşturun")
            confirm = st.text_input("🔒 Şifre Tekrar", type="password", placeholder="Şifrenizi tekrar girin")
            register_btn = st.form_submit_button("✅ Kayıt Ol", use_container_width=True)
            
            if register_btn:
                if not username or not password:
                    st.error("❌ Lütfen tüm alanları doldurun!")
                elif password != confirm:
                    st.error("❌ Şifreler uyuşmuyor!")
                elif len(password) < 6:
                    st.error("❌ Şifre en az 6 karakter olmalıdır!")
                elif register_user(username, hash_password(password)):
                    st.success("✅ Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
                else:
                    st.error("❌ Bu kullanıcı adı zaten mevcut!")

def view_patient_history(username):
    st.markdown("## 📋 Hasta Kayıtları")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Hasta Ara", placeholder="Hasta adı ile arama yapın...")
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Yenile", use_container_width=True):
            st.rerun()
    
    # Hasta verilerini yükle
    data = load_patients(username, search.strip() if search else None)
    
    # Debug bilgisi ekle
    st.write(f"Debug: {len(data)} kayıt bulundu")
    
    if not data:
        st.info("📭 Henüz kayıtlı hasta bulunmuyor.")
        # Veritabanında gerçekten kayıt var mı kontrol et
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM patients WHERE username = ?", (username,))
        total_count = c.fetchone()[0]
        conn.close()
        st.write(f"Debug: Toplam {total_count} kayıt var veritabanında")
        return

    st.markdown(f"**Toplam {len(data)} hasta kaydı bulundu**")
    
    for i, row in enumerate(data):
        pid, _, name, pred, prob, date, pdf = row
        
        with st.container():
            st.markdown("---")
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                st.markdown(f"### 👤 {name}")
                st.markdown(f"📅 **Tarih:** {date}")
            
            with col2:
                st.markdown(f"🔬 **Tahmin:** `{pred}`")
                st.markdown(f"📊 **Olasılık:** `%{prob}`")
            
            with col3:
                if pdf and os.path.exists(pdf):
                    try:
                        with open(pdf, "rb") as f:
                            st.download_button("📄 PDF İndir", f, file_name=os.path.basename(pdf), 
                                             key=f"pdf_{pid}_{i}", use_container_width=True)
                    except Exception as e:
                        st.warning(f"PDF okunamadı: {e}")
                else:
                    st.warning("📄 PDF bulunamadı")
            
            with col4:
                if st.button("🗑️ Sil", key=f"del_{pid}_{i}", use_container_width=True):
                    if delete_patient(pid):
                        st.success("✅ Hasta kaydı silindi.")
                        st.rerun()

def safe_encode_categorical(df, encoders):
    """Kategorik değişkenleri güvenli bir şekilde encode eder"""
    for col in df.columns:
        if df[col].dtype == object and col in encoders:
            try:
                encoder_classes = list(encoders[col].classes_)
                unknown_values = set(df[col].unique()) - set(encoder_classes)
                
                if unknown_values:
                    st.warning(f"'{col}' sütununda bilinmeyen değerler tespit edildi: {unknown_values}")
                    df[col] = df[col].replace(list(unknown_values), encoder_classes[0])
                
                df[col] = encoders[col].transform(df[col])
                
            except Exception as e:
                st.error(f"'{col}' sütunu encode edilirken hata: {e}")
                df[col] = 0
    
    return df

def main_app():
    st.markdown("# 🧬 Perisentez Tahmin Sistemi")
    st.markdown("*Prenatal genetik analiz ve sendrom tahmini için gelişmiş AI sistemi*")

    try:
        model = joblib.load("sendrom_lightgbm_model.pkl")
        encoders = joblib.load("encoders.pkl")
        target_encoder = joblib.load("target_encoder.pkl")
        feature_order = joblib.load("feature_order.pkl")
    except FileNotFoundError as e:
        st.error(f"❌ Model dosyaları bulunamadı: {e}")
        st.info("📝 Lütfen 'model_train.py' dosyasını çalıştırarak modelleri oluşturun.")
        return

    # Kategorik değişkenler
    cat_vars = [
        'Holoprosensefali', 'Yarık damak/dudak', 'Polidaktili', 'Polikistik böbrek',
        'Kardiyak defekt', 'Omfalosel', 'Mikrosefali', 'Cystic hygroma',
        'Tek umbilikal arter', 'IUGR', 'Ekstremite anomalisi', 'Ensefalosel',
        'Serebellar hipoplazi', 'Ventrikülomegali', 'Korpus kallozum agenezisi',
        'Makrosefali', 'Polihidramniyoz', 'Konjenital diyafragma hernisi',
        'Distal ekstremite hipoplazisi', 'Yüz dismorfizmi', 'Mikromeli',
        'Kraniofasiyal anomali', 'Kalp/böbrek defektleri', 'Böbrek anomalileri',
        'Genetik analiz (NIPBL)', 'Genetik analiz (ESCO2)', 'Genetik analiz (11p15)',
        'Makrozomi', 'Makroglossi'
    ]
    
    bin_opts = [0, 1]
    bin_labels = ["Yok", "Var"]
    
    sex_opts = [0, 1]
    sex_labels = ["Kız", "Erkek"]
    
    num_vars = [
        'β-hCG', 'PAPP-A', 'NT (Ense kalınlığı)', 'FL (Femur uzunluğu)', 'Anne yaşı',
        'Hafta', 'CRL', 'İleri kemik yaşı'
    ]

    input_data = {}
    
    # Ana form
    with st.form("prediction_form"):
        st.markdown("## 👶 Hasta Bilgileri")
        
        col1, col2 = st.columns(2)
        with col1:
            input_data["Hasta Adı"] = st.text_input("👤 Hasta Adı Soyadı", placeholder="Tam ad girin")
        with col2:
            sex_selection = st.selectbox("👶 Cinsiyet", bin_labels, index=0, 
                                       format_func=lambda x: "Kız" if x == "Yok" else "Erkek")
            input_data["Cinsiyet"] = 0 if sex_selection == "Yok" else 1

        st.markdown("## 🔬 Laboratuvar Değerleri")
        col1, col2 = st.columns(2)
        
        with col1:
            input_data["β-hCG"] = st.number_input("β-hCG (MoM)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
            input_data["PAPP-A"] = st.number_input("PAPP-A (MoM)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
            input_data["NT (Ense kalınlığı)"] = st.number_input("NT - Ense Kalınlığı (mm)", min_value=0.0, max_value=15.0, value=2.5, step=0.1)
            input_data["FL (Femur uzunluğu)"] = st.number_input("FL - Femur Uzunluğu (mm)", min_value=0.0, max_value=100.0, value=35.0, step=0.5)
        
        with col2:
            input_data["Anne yaşı"] = st.number_input("Anne Yaşı", min_value=15, max_value=50, value=28, step=1)
            input_data["Hafta"] = st.number_input("Gebelik Haftası", min_value=10, max_value=42, value=20, step=1)
            input_data["CRL"] = st.number_input("CRL (mm)", min_value=0.0, max_value=200.0, value=65.0, step=1.0)
            input_data["İleri kemik yaşı"] = st.number_input("İleri Kemik Yaşı (hafta)", min_value=0, max_value=10, value=0, step=1)

        st.markdown("## 🧬 Genetik ve Yapısal Bulgular")
        st.markdown("*Aşağıdaki bulgulardan mevcut olanları 'Var' olarak işaretleyin*")
        
        # Kategorik değişkenleri 3 sütunlu grid olarak düzenle
        num_cols = 3
        cols = st.columns(num_cols)
        
        for i, var in enumerate(cat_vars):
            with cols[i % num_cols]:
                selection = st.selectbox(
                    var, 
                    bin_labels, 
                    index=0,  # Default olarak "Yok" seçili
                    key=f"cat_{var}",
                    help=f"{var} bulgusu mevcut mu?"
                )
                input_data[var] = bin_opts[bin_labels.index(selection)]

        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submit = st.form_submit_button("🔍 Analiz Et ve Tahmin Yap", use_container_width=True)

    if submit:
        if not input_data["Hasta Adı"].strip():
            st.error("❌ Lütfen hasta adını girin.")
            return

        with st.spinner("🤖 AI modeli analiz yapıyor..."):
            try:
                df = pd.DataFrame([input_data])
                patient_name = df.pop("Hasta Adı").values[0]

                df = safe_encode_categorical(df, encoders)

                for feature in feature_order:
                    if feature not in df.columns:
                        df[feature] = 0 
                df = df[feature_order] 

                probs = model.predict_proba(df)[0]
                classes = target_encoder.inverse_transform(model.classes_)
                df_probs = pd.DataFrame({"Sendrom": classes, "Olasılık (%)": (probs * 100).round(2)})
                top_idx = probs.argmax()
                top_class = classes[top_idx]
                top_prob = probs[top_idx] * 100

                # Sonuçları göster
                st.success("✅ Analiz tamamlandı!")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"### 🎯 Tahmin Sonucu")
                    st.markdown(f"**Öngörülen Sendrom:** `{top_class}`")
                    st.markdown(f"**Güven Oranı:** `%{top_prob:.1f}`")
                
                with col2:
                    if top_prob > 70:
                        st.error("⚠️ Yüksek Risk")
                    elif top_prob > 50:
                        st.warning("⚡ Orta Risk")
                    else:
                        st.info("✅ Düşük Risk")

                explanation = generate_explanation(input_data, top_class)
                st.markdown("### 💡 AI Analiz Yorumu")
                st.info(explanation)

                st.markdown("### 📊 Detaylı Olasılık Analizi")
                df_probs_sorted = df_probs.sort_values(by="Olasılık (%)", ascending=False)
                
                for i, row in df_probs_sorted.head(5).iterrows():
                    progress_val = row['Olasılık (%)'] / 100
                    st.markdown(f"**{row['Sendrom']}**")
                    st.progress(progress_val)
                    st.markdown(f"`%{row['Olasılık (%)']:.2f}`")
                    st.markdown("---")

                # Grafik
                try:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    colors = ['#4A7C59' if i == 0 else '#7fb069' for i in range(len(df_probs_sorted.head(5)))]
                    bars = ax.barh(df_probs_sorted.head(5)["Sendrom"], df_probs_sorted.head(5)["Olasılık (%)"], color=colors)
                    ax.invert_yaxis()
                    ax.set_xlabel("Olasılık (%)", fontsize=12)
                    ax.set_title("Top 5 Sendrom Olasılıkları", fontsize=14, fontweight='bold')
                    ax.grid(axis='x', alpha=0.3)
                    
                    # Değerleri çubukların üzerine yaz
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                               f'%{width:.1f}', ha='left', va='center')
                    
                    st.pyplot(fig)
                    plt.close(fig)
                except Exception as e:
                    st.warning(f"Grafik çizilemedi: {e}")

                # PDF oluştur ve kaydet
                try:
                    pdf_file = generate_pdf(patient_name, top_class, top_prob, df_probs, st.session_state.username, explanation)
                    
                    if pdf_file and os.path.exists(pdf_file):
                        # Hasta kaydını veritabanına ekle
                        if save_patient(st.session_state.username, patient_name, top_class, top_prob, pdf_file):
                            st.success("✅ Hasta kaydı başarıyla veritabanına eklendi.")
                        else:
                            st.warning("⚠️ Hasta kaydı yapılamadı.")
                        
                        st.markdown("### 📄 Rapor İndirme")
                        with open(pdf_file, "rb") as f:
                            st.download_button("📥 PDF Raporunu İndir", f, 
                                             file_name=f"Perisentez_Raporu_{sanitize_text(patient_name).replace(' ', '_')}.pdf", 
                                             mime="application/pdf", use_container_width=True)
                    else:
                        st.error("❌ PDF oluşturulamadı.")
                        # PDF oluşturulamasa bile hasta kaydını kaydetmeye çalış
                        if save_patient(st.session_state.username, patient_name, top_class, top_prob, ""):
                            st.info("📝 Hasta kaydı PDF olmadan kaydedildi.")
                        else:
                            st.error("❌ Hasta kaydı da yapılamadı.")
                    
                except Exception as e:
                    st.error(f"⚠️ PDF/Kayıt hatası: {e}")
                    # Son çare: En basit şekilde hasta kaydını yap
                    try:
                        simple_name = ''.join(c for c in patient_name if c.isalnum() or c.isspace())
                        if save_patient(st.session_state.username, simple_name, top_class, top_prob, ""):
                            st.info("📝 Hasta kaydı basit formatta kaydedildi.")
                    except Exception as save_error:
                        st.error(f"❌ Hiçbir kayıt yapılamadı: {save_error}")

            except Exception as e:
                st.error(f"❌ Tahmin sırasında hata oluştu: {e}")
                st.info("📝 Lütfen girilen verileri kontrol edin ve tekrar deneyin.")

    # Hasta geçmişini göster
    st.markdown("---")
    if st.session_state.username:
        view_patient_history(st.session_state.username)

# Ana uygulama akışı
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Giriş Yap", use_container_width=True):
            st.session_state.page = "login"
    with col2:
        if st.button("👤 Kayıt Ol", use_container_width=True):
            st.session_state.page = "register"
    
    # Sayfa kontrolü
    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    if st.session_state.page == "login":
        login_screen()
    elif st.session_state.page == "register":
        register_screen()
        
        # Giriş ekranına dön butonu
        if st.button("← Giriş Ekranına Dön"):
            st.session_state.page = "login"
            st.rerun()

else:
    # Üst menü
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown(f"### 👋 Hoş geldiniz, **{st.session_state.username}**")
    
    with col2:
        if st.button("🏠 Ana Sayfa", use_container_width=True):
            st.session_state.current_page = "main"
            st.rerun()
    
    with col3:
        if st.button("🤖 AI Danışman", use_container_width=True):
            st.session_state.current_page = "chatbot"
            st.rerun()
    
    with col4:
        if st.button("🚪 Çıkış", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.current_page = "main"
            if "chat_history" in st.session_state:
                del st.session_state.chat_history
            st.rerun()
    
    # Sayfa kontrolü
    if "current_page" not in st.session_state:
        st.session_state.current_page = "main"
    
    st.markdown("---")
    
    if st.session_state.current_page == "main":
        main_app()
    elif st.session_state.current_page == "chatbot":
        chatbot_interface()
