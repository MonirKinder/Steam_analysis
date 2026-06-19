import psycopg2
from dotenv import load_dotenv
import os
import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

log.info("Connexion PostgreSQL établie")

clean_dir = Path("data/clean")
fichiers = sorted(clean_dir.glob("steamspy_clean_*.csv"))
dernier_fichier = fichiers[-1]

df = pd.read_csv(dernier_fichier)
log.info(f"Fichier chargé : {dernier_fichier} ({len(df)} lignes)")

cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO games (appid, name, developer, publisher)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (appid) DO NOTHING;
    """, (row["appid"], row["name"], row["developer"], row["publisher"]))

conn.commit()
log.info("Table games insérée")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO snapshots (
            appid, owners_lower, price_eur, discount,
            positive, negative, review_ratio,
            score_rank, average_forever, average_2weeks,
            median_forever, ccu
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        row["appid"],
        row["owners_lower"],
        row["price_eur"],
        row["discount"],
        row["positive"],
        row["negative"],
        row["review_ratio"],
        row["score_rank"],
        row["average_forever"],
        row["average_2weeks"],
        row["median_forever"],
        row["ccu"]
    ))

conn.commit()
log.info("Table snapshots insérée")

cursor.close()
conn.close()
log.info("Connexion fermée")