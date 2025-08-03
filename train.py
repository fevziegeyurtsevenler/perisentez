import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# 1. Veriyi oku
df = pd.read_csv(r"C:\Users\Sema\Desktop\Bootcamp\sentetik_sendrom_verisi_son.csv")  # Dosya adını gerektiğinde değiştir

# 2. Hedef değişken ve özellikler
target_column = "Hedef_Sendrom"
y = df[target_column]
X = df.drop(columns=[target_column])

# 3. Kategorik sütunları etiketle
label_encoders = {}
for col in X.select_dtypes(include="object").columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# 4. Hedef değişkeni encode et
target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

# 5. Veriyi eğitim ve test olarak ayır
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# 6. Modeli eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Özellik isimlerini al
feature_names = X.columns.tolist()

# 8. Tüm çıktıları kaydet
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("feature_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

with open("target_encoder.pkl", "wb") as f:
    pickle.dump(target_encoder, f)

with open("features.pkl", "wb") as f:
    pickle.dump(feature_names, f)

print("Model ve encoder dosyaları başarıyla kaydedildi.")
