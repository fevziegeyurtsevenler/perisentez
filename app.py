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



def sanitize_text(text):
    return (text
        .replace("ı", "i").replace("İ", "I")
        .replace("ş", "s").replace("Ş", "S")
        .replace("ç", "c").replace("Ç", "C")
        .replace("ğ", "g").replace("Ğ", "G")
        .replace("ü", "u").replace("Ü", "U")
        .replace("ö", "o").replace("Ö", "O")
    )


FONT_PATH = "DejaVuSansCondensed.ttf" 
FONT_NAME = "DejaVuSansCondensed"     

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        
        try:
            self.add_font(FONT_NAME, '', FONT_PATH, uni=True)
            self.set_font(FONT_NAME, '', 12)
        except Exception as e:
            st.error(f"Font yüklenirken bir hata oluştu. Lütfen '{FONT_PATH}' dosyasının doğru yolda olduğundan emin olun ve erişilebilirliğini kontrol edin. Hata: {e}")
            
            self.set_font("Arial", '', 12) 
            st.stop() 

    def chapter_title(self, title):
        self.set_font(FONT_NAME, '', 14)
        self.multi_cell(0, 10, txt=title, align='C')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font(FONT_NAME, '', 12)
        self.multi_cell(0, 8, txt=body)
        self.ln()


def generate_explanation(values, predicted_syndrome):
    comments = []

    
    if values["NT (Ense kalınlığı)"] > 3.5:
        comments.append(f"Ense kalınlığı {values['NT (Ense kalınlığı)']} mm olarak ölçülmüş, bu değer 3.5 mm üzeri olup nöral tüp defekti veya trizomilerle ilişkili olabilir.")

    if values["PAPP-A"] < 0.5:
        comments.append(f"PAPP-A seviyesi {values['PAPP-A']} MoM ile düşüktür; bu durum Down sendromu riskini artırabilir.")

    if values["β-hCG"] > 2.0:
        comments.append(f"β-hCG değeri {values['β-hCG']} MoM ile normalin üzerindedir, bu da trizomi 21 (Down) ile uyumlu olabilir.")

    if values["FL (Femur uzunluğu)"] < 15:
        comments.append(f"Femur uzunluğu {values['FL (Femur uzunluğu)']} mm olarak ölçülmüş ve kısa olması kemik gelişim bozukluklarına işaret edebilir.")

    
    if predicted_syndrome == "Patau":
        patau_specific_findings = []
        if values.get("Holoprosensefali") == "Var":
            patau_specific_findings.append("Holoprosensefali (ön beynin bölünmemesi)")
        if values.get("Yarık damak/dudak") == "Var":
            patau_specific_findings.append("Yarık damak/dudak")
        if values.get("Polidaktili") == "Var":
            patau_specific_findings.append("Polidaktili (fazla parmak)")
        if values.get("Kardiyak defekt") == "Var":
            patau_specific_findings.append("Kardiyak defekt")
        if values.get("Mikrosefali") == "Var":
            patau_specific_findings.append("Mikrosefali (küçük baş)")
        
        if patau_specific_findings:
            comments.append(f"Tahmin edilen Patau sendromu ile uyumlu olarak şu bulgulara rastlanmıştır: {', '.join(patau_specific_findings)}.")
        else:
            comments.append("Tahmin edilen Patau sendromu için spesifik bir genetik veya yapısal bulguya rastlanmamıştır. Ancak klinik bulgular ve diğer testler daha kapsamlı bir değerlendirme gerektirebilir.")
    
    elif predicted_syndrome == "Down":
        down_specific_findings = []
        if values.get("NT (Ense kalınlığı)") and values["NT (Ense kalınlığı)"] > 3.5:
             down_specific_findings.append("Artmış ense kalınlığı")
        if values.get("Kardiyak defekt") == "Var":
            down_specific_findings.append("Kardiyak defekt")
        if values.get("IUGR") == "Var":
            down_specific_findings.append("IUGR (intrauterin gelişme geriliği)")
        if values.get("PAPP-A") and values["PAPP-A"] < 0.5:
            down_specific_findings.append("Düşük PAPP-A seviyesi")
        if values.get("β-hCG") and values["β-hCG"] > 2.0:
            down_specific_findings.append("Yüksek β-hCG seviyesi")

        if down_specific_findings:
            comments.append(f"Tahmin edilen Down sendromu ile uyumlu olarak şu bulgulara rastlanmıştır: {', '.join(down_specific_findings)}.")
        else:
            comments.append("Tahmin edilen Down sendromu için spesifik bir bulguya rastlanmamıştır. Ancak klinik bulgular ve diğer testler daha kapsamlı bir değerlendirme gerektirebilir.")
    
    
    elif predicted_syndrome == "Edward":
        edward_specific_findings = []
        if values.get("IUGR") == "Var":
            edward_specific_findings.append("IUGR (intrauterin gelişme geriliği)")
        if values.get("Kardiyak defekt") == "Var":
            edward_specific_findings.append("Kardiyak defekt")
        if values.get("Polikistik böbrek") == "Var":
            edward_specific_findings.append("Polikistik böbrek")
        if values.get("Omfalosel") == "Var":
            edward_specific_findings.append("Omfalosel")
        
        if edward_specific_findings:
            comments.append(f"Tahmin edilen Edward sendromu ile uyumlu olarak şu bulgulara rastlanmıştır: {', '.join(edward_specific_findings)}.")
        else:
            comments.append("Tahmin edilen Edward sendromu için spesifik bir bulguya rastlanmamıştır. Ancak klinik bulgular ve diğer testler daha kapsamlı bir değerlendirme gerektirebilir.")
    
    
    elif predicted_syndrome == "DiGeorge":
        digeorge_specific_findings = []
        if values.get("Kardiyak defekt") == "Var":
            digeorge_specific_findings.append("Kardiyak defekt")
        if values.get("Yarık damak/dudak") == "Var":
            digeorge_specific_findings.append("Yarık damak/dudak")
        if values.get("Mikrosefali") == "Var":
            digeorge_specific_findings.append("Mikrosefali")
        
        if digeorge_specific_findings:
            comments.append(f"Tahmin edilen DiGeorge sendromu ile uyumlu olarak şu bulgulara rastlanmıştır: {', '.join(digeorge_specific_findings)}.")
        else:
            comments.append("Tahmin edilen DiGeorge sendromu için spesifik bir bulguya rastlanmamıştır. Ancak klinik bulgular ve diğer testler daha kapsamlı bir değerlendirme gerektirebilir.")

    if comments:
        explanation = "📌 **Yorum:** " + " ".join(comments)
    else:
        explanation = "ℹ️ Belirgin bir risk faktörü tespit edilmedi veya girilen verilerle doğrudan spesifik bir sendromla ilişkilendirilebilecek yeterli bulguya ulaşılamadı. Yapay zeka genel verilerle değerlendirme yapmıştır."
    return explanation




st.set_page_config(page_title="Perisentez", page_icon="🧬", layout="centered")

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
    c.execute("INSERT INTO patients (username, patient_name, prediction, probability, date, pdf_file) VALUES (?, ?, ?, ?, ?, ?)",
              (username, name, pred, f"%{prob:.1f}", datetime.now().strftime("%Y-%m-%d %H:%M"), pdf_file))
    conn.commit()
    conn.close()

def load_patients(username, search=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if search:
        c.execute("SELECT * FROM patients WHERE username = ? AND LOWER(patient_name) LIKE ? ORDER BY date DESC", (username, f"%{search.lower()}%"))
    else:
        c.execute("SELECT * FROM patients WHERE username = ? ORDER BY date DESC", (username,))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_patient(pid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM patients WHERE id = ?", (pid,))
    conn.commit()
    conn.close()


def generate_pdf(patient_name, result_class, result_prob, df_probs, doktor, explanation=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", '', 14)
    pdf.cell(200, 10, txt=sanitize_text("Perisentez Tahmin Raporu"), ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=sanitize_text(f"Hasta Adı: {patient_name}"), ln=True)
    pdf.cell(200, 10, txt=sanitize_text(f"Tahmin Edilen Sendrom: {result_class} (%{result_prob:.1f})"), ln=True)
    pdf.cell(200, 10, txt=sanitize_text(f"Doktor: {doktor}"), ln=True)
    pdf.cell(200, 10, txt=sanitize_text(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=sanitize_text("Tüm Olasılıklar:"), ln=True)

    if explanation:
        pdf.ln(5)
        pdf.multi_cell(0, 8, sanitize_text(explanation.replace("📌 **Yorum:** ", "")))

    pdf.ln(5)
    for _, row in df_probs.iterrows():
        pdf.cell(200, 10, txt=sanitize_text(f"{row['Sendrom']}: %{row['Olasılık (%)']}"), ln=True)

    pdf.ln(10)
    pdf.multi_cell(0, 10, sanitize_text(" Bu rapor ön tanı amaçlıdır. Kesin tanı için genetik danışmanlık önerilir."))

    fname = f"rapor_{sanitize_text(patient_name).replace(' ', '_')}_{uuid.uuid4().hex[:4]}.pdf"
    pdf.output(fname)
    return fname

def login_screen():
    st.image("logo.jpeg", width=150)
    st.markdown("## 🔐 Doktor Giriş Paneli")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if validate_login(username, hash_password(password)):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Hatalı giriş!")

def register_screen():
    st.markdown("## 👤 Kayıt Ol")
    username = st.text_input("Yeni Kullanıcı Adı")
    password = st.text_input("Yeni Şifre", type="password")
    confirm = st.text_input("Şifre Tekrar", type="password")
    if st.button("Kayıt Ol"):
        if password != confirm:
            st.error("Şifreler uyuşmuyor.")
        elif register_user(username, hash_password(password)):
            st.success("Kayıt başarılı.")
        else:
            st.error("Kullanıcı mevcut.")

def view_patient_history(username):
    
    st.markdown("## 🗂️ Kayıtlı Hastalar")
    search = st.text_input("🔍 Hasta Ara").strip()
    data = load_patients(username, search)
    
    if not data:
        st.info("Kayıt bulunamadı.")
        return

    for row in data:
        pid, _, name, pred, prob, date, pdf = row

        with st.container(border=True):
            st.markdown(f"### 👤 {name}")
            st.markdown(f"🔬 **Tahmin:** `{pred}`  \n📊 **Olasılık:** `{prob}`  \n📅 **Tarih:** `{date}`")

            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                if os.path.exists(pdf):
                    with open(pdf, "rb") as f:
                        st.download_button("📎 PDF İndir", f, file_name=pdf, key=f"pdf_{pid}")
                else:
                    st.warning("📎 PDF bulunamadı")

            with col2:
                if st.button("🗑️ Sil", key=f"del_{pid}"):
                    delete_patient(pid)
                    st.success("Hasta silindi.")
                    st.rerun()

            with col3:
                if st.button("🔍 Detay", key=f"det_{pid}"):
                    st.markdown(f"**Hasta Adı:** {name}  \n**Tahmin:** {pred} ({prob})  \n**Tarih:** {date}")


def main_app():
    st.markdown("# 🧬 Perisentez Tahmin Aracı")
    
    
    try:
        model = joblib.load("model.pkl")
        encoders = joblib.load("encoders.pkl")
        target_encoder = joblib.load("target_encoder.pkl")
        feature_order = joblib.load("feature_order.pkl")
    except FileNotFoundError:
        st.error("Model dosyaları bulunamadı. Lütfen 'model_train.py' dosyasını çalıştırarak modelleri oluşturun.")
        return

    cat_vars = ['Holoprosensefali', 'Yarık damak/dudak', 'Polidaktili', 'Polikistik böbrek',
                'Kardiyak defekt', 'Omfalosel', 'Mikrosefali', 'Cystic hygroma',
                'Tek umbilikal arter', 'IUGR']
    bin_opts = ["Var", "Yok"]
    sex_opts = ["Kız", "Erkek"]
    num_vars = ['β-hCG', 'PAPP-A', 'NT (Ense kalınlığı)', 'FL (Femur uzunluğu)', 'Anne yaşı', 'CRL']

    input_data = {}
    with st.form("form"):
        st.subheader("👶 Hasta Bilgileri")
        input_data["Hasta Adı"] = st.text_input("Ad Soyad")
        input_data["Cinsiyet"] = st.selectbox("Cinsiyet", sex_opts)

        with st.expander("Gelişimsel ve Yapısal Bulgular"):
            
            cols = st.columns(3)
            for i, v in enumerate(cat_vars):
                with cols[i % 3]:
                    input_data[v] = st.selectbox(v, bin_opts, key=f"cat_{v}")
        
        with st.expander("Laboratuvar ve Antropometrik Ölçümler"):
            
            cols = st.columns(2)
            for i, v in enumerate(num_vars):
                with cols[i % 2]:
                    
                    input_data[v] = st.number_input(v, format="%.2f", value=0.0, key=f"num_{v}")
        
        submit = st.form_submit_button("🔍 Tahmin Et")

    if submit:
        
        if not input_data["Hasta Adı"].strip():
            st.warning("Lütfen hasta adını girin.")
            return

        with st.spinner("Tahminler hesaplanıyor..."):
            df = pd.DataFrame([input_data])
            patient_name = df.pop("Hasta Adı").values[0]
            
            
            for col in df.columns:
                if df[col].dtype == object and col in encoders:
                    df[col] = encoders[col].transform(df[col])
            
            
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

        st.success(f"Tahmin: **{top_class}** (%{top_prob:.1f})")
        
        
        explanation = generate_explanation(input_data, top_class)
        st.markdown("### 💡 Yapay Zeka Yorumu")
        st.info(explanation)

        st.markdown("### 📊 Tüm Olasılıklar")
        
        df_probs_sorted = df_probs.sort_values(by="Olasılık (%)", ascending=False)
        for _, row in df_probs_sorted.iterrows():
            st.markdown(f"- **{row['Sendrom']}**: %{row['Olasılık (%)']:.2f}")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(df_probs_sorted["Sendrom"], df_probs_sorted["Olasılık (%)"], color="#4A7C59")
        ax.invert_yaxis()
        ax.set_xlabel("Olasılık (%)")
        ax.set_title("Sendrom Olasılıkları")
        st.pyplot(fig)

        
        pdf_file = generate_pdf(patient_name, top_class, top_prob, df_probs, st.session_state.username, explanation)
        save_patient(st.session_state.username, patient_name, top_class, top_prob, pdf_file)
        
        with open(pdf_file, "rb") as f:
            st.download_button("⬇️ PDF Raporunu İndir", f, file_name=os.path.basename(pdf_file), mime="application/pdf")
        
        

    view_patient_history(st.session_state.username)


menu = st.sidebar.selectbox("Menü", ["Giriş Yap", "Kayıt Ol"] if not st.session_state.authenticated else ["Tahmin Aracı", "Çıkış"])
if not st.session_state.authenticated:
    if menu == "Giriş Yap": login_screen()
    elif menu == "Kayıt Ol": register_screen()
else:
    if menu == "Tahmin Aracı": main_app()
    elif menu == "Çıkış":
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
