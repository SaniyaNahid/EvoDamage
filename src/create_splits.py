from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


INPUT = "data/processed/labels.csv"
OUTPUT = Path("data/splits")

OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

train, temp = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)

val, test = train_test_split(
    temp,
    test_size=0.50,
    random_state=42,
    stratify=temp["label"]
)

train.to_csv(OUTPUT / "train.csv", index=False)
val.to_csv(OUTPUT / "val.csv", index=False)
test.to_csv(OUTPUT / "test.csv", index=False)

print("Train:", len(train))
print("Validation:", len(val))
print("Test:", len(test))