import pandas as pd
from pathlib import Path
from datetime import datetime


raw_dir = Path("data/raw")
clean_dir = Path("data/clean")

clean_dir.mkdir(parents=True, exist_ok=True)         #crée le dossier clean s'il n'existe pas déjà
timestamp = datetime.now().strftime("%Y%m%d_%H%M")  #format de timestamp pour le nom du fichier de sortie
output_file = clean_dir / f"steamspy_clean_{timestamp}.csv"  #chemin du fichier de sortie

fichiers = sorted(raw_dir.glob("steamspy_*.csv"))    #trie les fichiers par ordre alphabétique, pour recupérer le dernier fichier
dernier_fichier = fichiers[-1]


df = pd.read_csv(dernier_fichier)
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())


#clean owners---------------------------------------------
print('owners')
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
#print('price')
#print(df["price"].head(10))
#print(df["price"].dtype)

df["price_eur"] = (df["price"] / 100).round(2)
print('price_eur')
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

print('review_ratio')
print(df["review_ratio"].head(10))


#clean dulpluicates no name---------------------------------------------
df = df.drop_duplicates(subset="appid", keep="first")
df = df[df["name"].notna()]
df = df[(df["owners_lower"] != 0) | (df["positive"] != 0)]





colonnes_finales = [
    "appid",
    "name",
    "developer",
    "publisher",
    "owners_lower",
    "price_eur",
    "discount",
    "positive",
    "negative",
    "review_ratio",
    "score_rank",
    "average_forever",
    "average_2weeks",
    "median_forever",
    "ccu"
]

df = df[colonnes_finales]
print(df.shape)
print(df.head())



df.to_csv(output_file, index=False, encoding="utf-8")
print(f"Fichier propre sauvegardé : {output_file}")