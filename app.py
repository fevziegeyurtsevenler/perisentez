import streamlit as st
import pandas as pd
import joblib
import uuid
import os
import hashlib
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import json
import base64

def generate_html_report(patient_name, result_class, result_prob, df_probs, doktor, explanation=None):
    """HTML raporu oluşturur - PDF yerine daha güvenilir"""
    try:
        # HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Perisentez Tahmin Raporu</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                    color: #333;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #4A7C59;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .title {{
                    color: #4A7C59;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .info-section {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }}
                .result-highlight {{
                    background-color: #e8f5e8;
                    border-left: 4px solid #4A7C59;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .probability-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                .probability-table th, .probability-table td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                .probability-table th {{
                    background-color: #4A7C59;
                    color: white;
                }}
                .probability-table tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .explanation {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-style: italic;
                    color: #666;
                }}
                .risk-level {{
                    display: inline-block;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-weight: bold;
                    color: white;
                }}
                .high-risk {{ background-color: #dc3545; }}
                .medium-risk {{ background-color: #ffc107; color: #000; }}
                .low-risk {{ background-color: #28a745; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">🧬 Perisentez Tahmin Raporu</div>
                <p>Prenatal Genetik Analiz Sonuçları</p>
            </div>
            
            <div class="info-section">
                <h3>👤 Hasta Bilgileri</h3>
                <p><strong>Hasta Adı:</strong> {patient_name}</p>
                <p><strong>Doktor:</strong> {doktor}</p>
                <p><strong>Rapor Tarihi:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
            </div>
            
            <div class="result-highlight">
                <h3>🎯 Ana Tahmin Sonucu</h3>
                <p><strong>Öngörülen Sendrom:</strong> {result_class}</p>
                <p><strong>Güven Oranı:</strong> %{result_prob:.1f}</p>
                <p><strong>Risk Seviyesi:</strong> 
                    <span class="risk-level {'high-risk' if result_prob > 70 else 'medium-risk' if result_prob > 50 else 'low-risk'}">
                        {'Yüksek Risk' if result_prob > 70 else 'Orta Risk' if result_prob > 50 else 'Düşük Risk'}
                    </span>
                </p>
            </div>
        """
        
        # Açıklama varsa ekle
        if explanation:
            html_content += f"""
            <div class="explanation">
                <h4>💡 AI Analiz Yorumu</h4>
                <p>{explanation}</p>
            </div>
            """
        
        # Olasılık tablosu
        html_content += """
            <h3>📊 Detaylı Olasılık Analizi</h3>
            <table class="probability-table">
                <thead>
                    <tr>
                        <th>Sendrom</th>
                        <th>Olasılık (%)</th>
                        <th>Değerlendirme</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Olasılıkları sırala ve tabloya ekle
        df_sorted = df_probs.sort_values(by="Olasılık (%)", ascending=False)
        for idx, row in df_sorted.iterrows():
            prob_val = row['Olasılık (%)']
            evaluation = "Yüksek" if prob_val > 50 else "Orta" if prob_val > 20 else "Düşük"
            html_content += f"""
                    <tr>
                        <td>{row['Sendrom']}</td>
                        <td>%{prob_val:.2f}</td>
                        <td>{evaluation}</td>
                    </tr>
            """
        
        html_content += """
                </tbody>
            </table>
            
            <div class="footer">
                <p><strong>⚠️ Önemli Uyarı:</strong> Bu rapor ön tanı amaçlıdır ve kesin tanı için genetik danışmanlık önerilir. 
                Sonuçlar yapay zeka algoritması tarafından oluşturulmuş olup, klinik karar vermede tek başına kullanılmamalıdır.</p>
                <p><strong>Sistem:</strong> Perisentez AI Tahmin Sistemi v1.0</p>
            </div>
        </body>
        </html>
        """
        
        # Dosya adını güvenli hale getir
        safe_name = ''.join(c for c in patient_name if c.isalnum() or c.isspace()).replace(' ', '_')
        if not safe_name:
            safe_name = "hasta"
        
        filename = f"rapor_{safe_name}_{uuid.uuid4().hex[:6]}.html"
        
        # HTML dosyasını kaydet
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
        
    except Exception as e:
        st.error(f"HTML raporu oluşturulurken hata: {e}")
        return None

def generate_explanation(values, predicted_syndrome):
    """AI analiz yorumu oluştur"""
    comments = []

    if values.get("NT (Ense kalınlığı)", 0) > 3.5:
        comments.append(f"Ense kalınlığı {values['NT (Ense kalınlığı)']} mm olarak ölçülmüş, bu değer 3.5 mm üzeri olup nöral tüp defekti veya trizomilerle ilişkili olabilir.")
    
    if values.get("PAPP-A", 1) < 0.5:
        comments.append(f"PAPP-A seviyesi {values['PAPP-A']} MoM ile düşüktür; bu durum Down sendromu riskini artırabilir.")
    
    if values.get("β-hCG", 0) > 2.0:
        comments.append(f"β-hCG değeri {values['β-hCG']} MoM ile normalin üzerindedir, bu da trizomi 21 (Down) ile uyumlu olabilir.")
    
    if values.get("FL (Femur uzunluğu)", 1000) < 15:
        comments.append(f"Femur uzunluğu {values['FL (Femur uzunluğu)']} mm olarak ölçülmüş ve kısa olması kemik gelişim bozukluklarına işaret edebilir.")
    
    if values.get("Anne yaşı", 0) > 35:
        comments.append(f"Anne yaşı {values['Anne yaşı']} olup, ileri maternal yaş kromozomal anomali riskini artırır.")

    if comments:
        explanation = "📌 **Yorum:** " + " ".join(comments)
    else:
        explanation = "ℹ️ Belirgin bir risk faktörü tespit edilmedi. Girilen parametreler normal sınırlar içerisindedir. Yapay zeka modeli genel verilerle değerlendirme yapmıştır."
    
    return explanation

# AI Danışman fonksiyonları - app.py tarzında güncelleme

def get_gemini_key():
    """Gemini API anahtarını döndür"""
    # Hardcoded API key from app.py
    return "AIzaSyCN1-ZR9SEz3o88sdBRy4tn_gpfndrfpXw"

def call_gemini_api(prompt, api_key):
    """Google Gemini API çağrısı (app.py tarzında sadeleştirilmiş)"""
    if not api_key:
        return "Gemini API anahtarı bulunamadı."
    try:
        # Corrected Gemini API endpoint for generateContent
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        
        # Constructing the request body according to Gemini API for text-only input
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": (
                            "Sen bir tıbbi danışman asistanısın. Perinatology, genetik sendromlar, "
                            "prenatal tanı ve perisentez konularında uzmanlaşmış durumdasın. "
                            "Verdiğin bilgiler sadece eğitim amaçlıdır ve kesin tanı için doktora başvurulması gerektiğini belirt."
                        )},
                        {"text": f"Soru: {prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            res = response.json()
            if "candidates" in res and len(res["candidates"]) > 0:
                candidate = res["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "text" in part:
                            return part["text"]
            return "Gemini API'den beklenen yanıt formatı alınamadı."
        else:
            return f"API Hatası: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Hata: {str(e)}"

def chatbot_interface():
    """Chatbot arayüzü - app.py tarzında sadeleştirilmiş (sadece Google Gemini)"""
    st.markdown("## 🤖 AI Danışman Chatbot (Sadece Google Gemini)")
    
    # Chat geçmişi
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Soru giriş alanı
    user_question = st.text_area("Sorunuzu yazın:", height=100, 
                                placeholder="Örn: Down sendromu hakkında bilgi verir misiniz?")
    
    if st.button("📨 Gönder", use_container_width=True):
        if user_question.strip():
            # The prompt is now directly passed to call_gemini_api; the system context is handled there.
            full_prompt = user_question 
            with st.spinner("Gemini yanıt oluşturuyor..."):
                api_key = get_gemini_key()
                response = call_gemini_api(full_prompt, api_key)
                st.session_state.chat_history.append({"user": user_question, "ai": response})
                st.rerun()
    
    if st.button("🗑️ Geçmişi Temizle", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    # Chat geçmişini gösterme
    if st.session_state.chat_history:
        st.markdown("### 💬 Sohbet Geçmişi (Son 5)")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
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

def save_patient(username, name, pred, prob, report_file):
    """Hasta kaydını veritabanına kaydet"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        clean_prob = f"{float(prob):.1f}"
        
        c.execute("INSERT INTO patients (username, patient_name, prediction, probability, date, pdf_file) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, name, pred, clean_prob, current_date, report_file))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Hasta kaydedilirken hata: {e}")
        return False
    finally:
        conn.close()

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
    """Hasta kaydını sil"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Rapor dosyasını da sil
        c.execute("SELECT pdf_file FROM patients WHERE id = ?", (pid,))
        result = c.fetchone()
        if result and result[0] and os.path.exists(result[0]):
            os.remove(result[0])
        
        c.execute("DELETE FROM patients WHERE id = ?", (pid,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Hasta silinirken hata: {e}")
        return False
    finally:
        conn.close()

def login_screen():
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="color: #4A7C59;">🧬 Perisentez Tahmin Sistemi</h1>
            <p style="font-size: 1.2rem; color: #666;">Prenatal Genetik Analiz Platformu</p>
        </div>
    """, unsafe_allow_html=True)
    
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
    """Hasta geçmişini görüntüle"""
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
    
    if not data:
        st.info("📭 Henüz kayıtlı hasta bulunmuyor.")
        # Debug: Toplam kayıt sayısını kontrol et
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM patients WHERE username = ?", (username,))
        total_count = c.fetchone()[0]
        conn.close()
        if total_count > 0:
            st.warning(f"Veritabanında {total_count} kayıt var ama görüntülenemiyor. Arama kriterini kontrol edin.")
        return

    st.markdown(f"**📊 Toplam {len(data)} hasta kaydı bulundu**")
    
    for i, row in enumerate(data):
        pid, _, name, pred, prob, date, report_file = row
        
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
                if report_file and os.path.exists(report_file):
                    try:
                        with open(report_file, "rb") as f:
                            file_extension = os.path.splitext(report_file)[1].lower()
                            mime_type = "text/html" if file_extension == ".html" else "application/pdf"
                            download_name = f"Rapor_{name.replace(' ', '_')}{file_extension}"
                            
                            st.download_button(
                                "📄 Rapor İndir", 
                                f, 
                                file_name=download_name,
                                mime=mime_type,
                                key=f"report_{pid}_{i}", 
                                use_container_width=True
                            )
                    except Exception as e:
                        st.warning(f"Dosya okunamadı: {e}")
                else:
                    st.warning("📄 Rapor bulunamadı")
            
            with col4:
                if st.button("🗑️ Sil", key=f"del_{pid}_{i}", use_container_width=True):
                    if delete_patient(pid):
                        st.success("✅ Hasta kaydı silindi.")
                        st.rerun()
                    else:
                        st.error("❌ Silme işlemi başarısız.")

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
        model = joblib.load(r"C:\Users\Sema\Desktop\Bootcamp\yeni\model.pkl")
        encoders = joblib.load(r"C:\Users\Sema\Desktop\Bootcamp\yeni\feature_encoders.pkl")
        target_encoder = joblib.load(r"C:\Users\Sema\Desktop\Bootcamp\yeni\target_encoder.pkl")
        feature_order = joblib.load(r"C:\Users\Sema\Desktop\Bootcamp\yeni\features.pkl")
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

                # HTML raporu oluştur ve kaydet
                try:
                    report_file = generate_html_report(patient_name, top_class, top_prob, df_probs, st.session_state.username, explanation)
                    
                    if report_file and os.path.exists(report_file):
                        # Hasta kaydını veritabanına ekle
                        if save_patient(st.session_state.username, patient_name, top_class, top_prob, report_file):
                            st.success("✅ Hasta kaydı başarıyla veritabanına eklendi.")
                        else:
                            st.warning("⚠️ Hasta kaydı yapılamadı.")
                        
                        st.markdown("### 📄 Rapor İndirme")
                        # HTML dosyasını okuyup indirme butonu oluştur
                        with open(report_file, "rb") as f:
                            st.download_button(
                                "📥 HTML Raporunu İndir", 
                                f, 
                                file_name=f"Perisentez_Raporu_{patient_name.replace(' ', '_')}.html", 
                                mime="text/html", 
                                use_container_width=True
                            )
                        
                        # Raporu inline olarak gösterme seçeneği
                        if st.checkbox("📖 Raporu burada göster"):
                            with open(report_file, "r", encoding='utf-8') as f:
                                html_content = f.read()
                            st.components.v1.html(html_content, height=800, scrolling=True)
                            
                    else:
                        st.error("❌ Rapor oluşturulamadı.")
                        # Rapor oluşturulamasa bile hasta kaydını kaydetmeye çalış
                        if save_patient(st.session_state.username, patient_name, top_class, top_prob, ""):
                            st.info("📝 Hasta kaydı rapor olmadan kaydedildi.")
                        else:
                            st.error("❌ Hasta kaydı da yapılamadı.")
                    
                except Exception as e:
                    st.error(f"⚠️ Rapor/Kayıt hatası: {e}")
                    # Son çare: En basit şekilde hasta kaydını yap
                    try:
                        if save_patient(st.session_state.username, patient_name, top_class, top_prob, ""):
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
