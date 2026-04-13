import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, ConfusionMatrixDisplay)
from sklearn.preprocessing import LabelEncoder

# ─── 1. Load Data ───────────────────────────────────────────────
df = pd.read_csv("C:\\Users\\dell\\Desktop\\AI Based CPU Schedular\\data\\processes_dataset.csv")

FEATURES = [
    "cpu_burst_time",
    "io_burst_time",
    "io_frequency",
    "execution_cycles",
    "priority",
    "cpu_io_ratio"
]
LABEL = "process_type"

X = df[FEATURES]
y = df[LABEL]

# Encode labels: CPU-bound=0, IO-bound=1
le = LabelEncoder()
y_enc = le.fit_transform(y)

# ─── 2. Train / Test Split (80 / 20) ────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

# ─── 3. Train Random Forest ─────────────────────────────────────
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# ─── 4. Evaluate ────────────────────────────────────────────────
y_pred      = model.predict(X_test)
accuracy    = accuracy_score(y_test, y_pred)
cv_scores   = cross_val_score(model, X, y_enc, cv=5, scoring="accuracy")

print("=" * 55)
print("        Random Forest — Training Complete")
print("=" * 55)
print(f"  Training samples  : {len(X_train)}")
print(f"  Testing  samples  : {len(X_test)}")
print()
print(f"  Test  Accuracy    : {accuracy * 100:.2f}%")
print(f"  CV    Accuracy    : {cv_scores.mean() * 100:.2f}%  "
      f"(±{cv_scores.std() * 100:.2f}%)")
print()
print("  Classification Report:")
print(classification_report(
    y_test, y_pred,
    target_names=le.classes_,
    digits=4
))

# ─── 5. Feature Importance ──────────────────────────────────────
importances = pd.Series(model.feature_importances_, index=FEATURES)
importances = importances.sort_values(ascending=False)

print("  Feature Importances:")
for feat, val in importances.items():
    bar = "█" * int(val * 60)
    print(f"    {feat:<22} {val:.4f}  {bar}")
print()

# ─── 6. Save Model & Encoder ────────────────────────────────────
joblib.dump(model, "C:\\Users\\dell\\Desktop\\AI Based CPU Schedular\\model\\scheduler_model.pkl")
joblib.dump(le,    "C:\\Users\\dell\\Desktop\\AI Based CPU Schedular\\model\\label_encoder.pkl")
print("  Model saved  → model/scheduler_model.pkl")
print("  Encoder saved→ model/label_encoder.pkl")
print("=" * 55)

# ─── 7. Plots ───────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Random Forest — Model Evaluation", fontsize=14, fontweight="bold")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                display_labels=le.classes_)
disp.plot(ax=axes[0], colorbar=False, cmap="Blues")
axes[0].set_title("Confusion Matrix")

# Feature Importance bar chart
colors = ["#4a86e8" if i == 0 else "#6aa3f5"
            for i in range(len(importances))]
axes[1].barh(importances.index[::-1],
                importances.values[::-1],
                color=colors[::-1], edgecolor="white")
axes[1].set_title("Feature Importance")
axes[1].set_xlabel("Importance Score")
for i, v in enumerate(importances.values[::-1]):
    axes[1].text(v + 0.002, i, f"{v:.3f}", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("C:\\Users\\dell\\Desktop\\AI Based CPU Schedular\\model\\model_evaluation.png",
            dpi=150, bbox_inches="tight")
print("  Chart saved  → model/model_evaluation.png")
