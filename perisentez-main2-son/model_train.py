
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# Veriyi oku
df = pd.read_csv("veri.csv")

# Kategorik sütunları sayısala çevir
encoders = {}
for col in df.columns:
    if df[col].dtype == "object" and col != "Sendrom":
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

# Hedef değişkeni encode et
target_encoder = LabelEncoder()
df["Sendrom"] = target_encoder.fit_transform(df["Sendrom"])

# Özellikler ve hedef ayrımı
X = df.drop("Sendrom", axis=1)
y = df["Sendrom"]

# Eğitim ve test bölmesi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model eğitimi
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Model ve encoder'ları kaydet
joblib.dump(model, "model.pkl")
joblib.dump(encoders, "encoders.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")
joblib.dump(X.columns.tolist(), "feature_order.pkl")

print("Model, encoderlar ve feature sırası başarıyla kaydedildi.")
