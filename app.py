
import streamlit as st
import pandas as pd
import joblib
import uuid
from datetime import datetime
from fpdf import FPDF
import os
import hashlib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Perisentez", page_icon="🧬", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

USER_FILE = "users.csv"
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_FILE, index=False)

def load_users():
    return pd.read_csv(USER_FILE)

def save_user(username, password):
    df = load_users()
    df = pd.concat([df, pd.DataFrame([{"username": username, "password": password}])], ignore_index=True)
    df.to_csv(USER_FILE, index=False)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def sanitize_text(text):
    return (text
        .replace("ı", "i").replace("İ", "I")
        .replace("ş", "s").replace("Ş", "S")
        .replace("ç", "c").replace("Ç", "C")
        .replace("ğ", "g").replace("Ğ", "G")
        .replace("ü", "u").replace("Ü", "U")
        .replace("ö", "o").replace("Ö", "O")
    )

def login_screen():
    st.markdown("<h2 style='text-align: center;'>🔐 Doktor Giriş Paneli</h2>", unsafe_allow_html=True)
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        users = load_users()
        pw_hash = hash_password(password)
        if ((users["username"] == username) & (users["password"] == pw_hash)).any():
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Giriş başarılı.")
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre.")

def register_screen():
    st.markdown("### 👤 Kayıt Ol")
    username = st.text_input("Yeni Kullanıcı Adı")
    password = st.text_input("Yeni Şifre", type="password")
    confirm = st.text_input("Şifre Tekrar", type="password")
    if st.button("Kayıt Ol"):
        if password != confirm:
            st.error("Şifreler uyuşmuyor.")
            return
        users = load_users()
        if username in users["username"].values:
            st.error("Bu kullanıcı adı zaten alınmış.")
        else:
            save_user(username, hash_password(password))
            st.success("Kayıt başarılı! Giriş yapabilirsiniz.")

def generate_pdf(patient_name, result_class, result_prob, all_probs, doktor):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Perisentez Tahmin Raporu", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=sanitize_text(f"Hasta Adı: {patient_name}"), ln=True)
    pdf.cell(200, 10, txt=sanitize_text(f"Tahmin Edilen Sendrom: {result_class} (%{result_prob:.1f})"), ln=True)
    pdf.cell(200, 10, txt=sanitize_text(f"Doktor: {doktor}"), ln=True)
    pdf.cell(200, 10, txt=sanitize_text(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=sanitize_text("Tüm Olasılıklar:"), ln=True)
    for idx, row in all_probs.iterrows():
        line = f"{row['Sendrom']}: %{row['Olasılık (%)']}"
        pdf.cell(200, 10, txt=sanitize_text(line), ln=True)
    file_name = f"rapor_{uuid.uuid4().hex[:8]}.pdf"
    pdf.output(file_name)
    return file_name

def save_patient(username, patient_name, sendrom, prob, all_probs_file):
    fname = f"patients_{username}.csv"
    new_row = {
        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Hasta Adı": patient_name,
        "Tahmin": sendrom,
        "Olasılık": f"%{prob:.1f}",
        "PDF": all_probs_file
    }
    if os.path.exists(fname):
        df = pd.read_csv(fname)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    df.to_csv(fname, index=False)



def view_patient_history(username):
    st.markdown("### 🗂️ Kayıtlı Hastalar")
    fname = f"patients_{username}.csv"
    if not os.path.exists(fname):
        st.info("Henüz hasta kaydı yok.")
        return

    df = pd.read_csv(fname)
    if df.empty:
        st.info("Kayıtlı hasta bulunamadı.")
        return

    search_term = st.text_input("🔍 Hasta Arama", placeholder="Hasta adı girin...").lower().strip()
    if search_term:
        df = df[df["Hasta Adı"].str.lower().str.contains(search_term)]

    if df.empty:
        st.warning("Aramanıza uygun hasta bulunamadı.")
        return

    for i, row in df.iterrows():
        with st.container(border=True):
            cols = st.columns([3, 2, 2, 1])
            cols[0].markdown(f"**👤 {row['Hasta Adı']}**")
            cols[1].markdown(f"🧬 Tahmin: **{row['Tahmin']}**")
            cols[2].markdown(f"📅 {row['Tarih']}")
            with cols[3]:
                
                if os.path.exists(row["PDF"]):
                    with open(row["PDF"], "rb") as f:
                        st.download_button("📄", f, file_name=row["PDF"], key=f"pdf_{i}", use_container_width=True)
                else:
                    st.warning("📄 PDF bulunamadı.")

            col_det, col_del = st.columns([1, 1])
            with col_det:
                if st.button("🔍 Detay", key=f"detay_{i}"):
                    st.markdown("##### 📋 Tahmin Özeti")
                    st.write(f"- Hasta: **{row['Hasta Adı']}**")
                    st.write(f"- Tarih: {row['Tarih']}")
                    st.write(f"- Sendrom Tahmini: {row['Tahmin']} {row['Olasılık']}")
            with col_del:
                if st.button("🗑️ Sil", key=f"sil_{i}"):
                    df.drop(index=row.name, inplace=True)
                    df.to_csv(fname, index=False)
                    st.success("Kayıt silindi.")
                    st.rerun()

def main_app():
    st.markdown("<h1 style='text-align: center; color: #4A7C59;'>🧬 Perisentez</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Yapay Zeka Destekli Genetik Sendrom Tahmini</h4>", unsafe_allow_html=True)
    st.markdown("---")

    model = joblib.load("model.pkl")
    encoders = joblib.load("encoders.pkl")
    target_encoder = joblib.load("target_encoder.pkl")
    feature_order = joblib.load("feature_order.pkl")

    categorical_vars = [
        'Holoprosensefali', 'Yarık damak/dudak', 'Polidaktili', 'Polikistik böbrek',
        'Kardiyak defekt', 'Omfalosel', 'Mikrosefali', 'Cystic hygroma',
        'Tek umbilikal arter', 'IUGR'
    ]
    binary_options = ["Var", "Yok"]
    sex_options = ["Kız", "Erkek"]
    numerical_vars = [
        'β-hCG', 'PAPP-A', 'NT (Ense kalınlığı)',
        'FL (Femur uzunluğu)', 'Anne yaşı', 'CRL'
    ]

    input_data = {}
    with st.form("sendrom_form"):
        st.subheader("👶 Hasta Bilgileri")
        patient_name = st.text_input("Hasta Adı Soyadı")

        st.subheader("📋 Anatomik ve Genetik Bulgular")
        col1, col2 = st.columns(2)
        for i, cat in enumerate(categorical_vars):
            with col1 if i % 2 == 0 else col2:
                input_data[cat] = st.selectbox(f"{cat}", binary_options)

        input_data["Cinsiyet"] = st.selectbox("Cinsiyet", sex_options)

        st.subheader("📈 Sayısal Parametreler")
        col3, col4 = st.columns(2)
        for i, num in enumerate(numerical_vars):
            with col3 if i % 2 == 0 else col4:
                input_data[num] = st.number_input(num, format="%.2f")

        submitted = st.form_submit_button("🔍 Tahmin Et")

    if submitted:
        df_input = pd.DataFrame([input_data])
        for col in df_input.columns:
            if col in encoders:
                df_input[col] = encoders[col].transform(df_input[col])
        df_input = df_input[feature_order]

        probs = model.predict_proba(df_input)[0]
        classes = target_encoder.inverse_transform(model.classes_)
        top_idx = probs.argmax()
        top_class = classes[top_idx]
        top_prob = probs[top_idx] * 100

        st.markdown("### 🎯 Tahmin Sonucu")
        st.success(f"**{top_class}** (%{top_prob:.1f} olasılıkla)")

    st.markdown("#### 🔎 Diğer Olasılıklar:")
    other_probs = df_probs[df_probs["Sendrom"] != top_class]
    for _, row in other_probs.iterrows():
        st.markdown(f"- {row['Sendrom']}: **%{row['Olasılık (%)']}**")
    st.markdown("#### 🔎 Diğer Olasılıklar:")
    for _, row in df_probs.iterrows():
        st.markdown(f"- {row['Sendrom']}: **%{row['Olasılık (%)']}**")

        df_probs = pd.DataFrame({
            "Sendrom": classes,
            "Olasılık (%)": (probs * 100).round(2)
        }).sort_values("Olasılık (%)", ascending=False)

        st.markdown("### 📊 Olasılık Dağılımı")
        fig, ax = plt.subplots()
        ax.barh(df_probs["Sendrom"], df_probs["Olasılık (%)"], color="#4A7C59")
        ax.invert_yaxis()
        ax.set_xlabel("Olasılık (%)")
        ax.set_xlim(0, 100)
        st.pyplot(fig)

        pdf_file = generate_pdf(patient_name, top_class, top_prob, df_probs, st.session_state.username)
        save_patient(st.session_state.username, patient_name, top_class, top_prob, pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("⬇️ PDF Raporu İndir", f, file_name=pdf_file, mime="application/pdf")
        # os.remove(pdf_file)  # Artık silinmiyor

    st.markdown("---")
    view_patient_history(st.session_state.username)

menu = st.sidebar.selectbox("Menü", ["Giriş Yap", "Kayıt Ol"] if not st.session_state.authenticated else ["Tahmin Aracı", "Çıkış"])

if not st.session_state.authenticated:
    if menu == "Giriş Yap":
        login_screen()
    elif menu == "Kayıt Ol":
        register_screen()
else:
    if menu == "Tahmin Aracı":
        main_app()
    elif menu == "Çıkış":
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
