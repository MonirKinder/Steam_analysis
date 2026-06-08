import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw")
fichiers = sorted(raw_dir.glob("steamspy_*.csv"))
dernier_fichier = fichiers[-1]


df = pd.read_csv(dernier_fichier)
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())


#clean owners---------------------------------------------
print(df["owners"].head(10))

df["owners_lower"] = (
        df["owners"]
        .str.split(" .. ")  # sépare la chaîne en deux parties
        .str[0]
        .str.replace(",", "")
        .str.strip()                # retire les espaces avant et après
        .astype(int)
        )

print(df["owners_lower"].head(10))

#clean price---------------------------------------------
print('price')
print(df["price"].head(10))
print(df["price"].dtype)

df["price_eur"] = (df["price"] / 100).round(2)
print(df["price_eur"].head(10))

#clean developer et publisher score rank---------------------------------------------
df["developer"] = df["developer"].fillna("Unknown")
df["publisher"] = df["publisher"].fillna("Unknown")
df["score_rank"] = df["score_rank"].fillna(0).astype(int)

#ratio ---------------------------------------------*
total= df["positive"] + df["negative"]
df["review_ratio"] = (
    df["positive"]
    .astype(float)
    .div(total.replace(0, float("nan")))
    .round(4)
    )

print(df["review_ratio"])
print(df["review_ratio"].head(10))


#clean dulpluicates no name---------------------------------------------
df = df.drop_duplicates(subset="appid", keep="first")
df = df[df["name"].notna()]
df = df[~((df["owners_lower"] == 0) & (df["positive"] == 0))]