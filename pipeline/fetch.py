import requests 
import csv
import time
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

url = "https://steamspy.com/api.php"
all_games=[]

for page in range (0,3):
    parametres={
        "request": "all",
        "page": page}

    try:
        response = requests.get(url, params=parametres)
        response.raise_for_status()  #declenche une exception pour les codes d'erreur HTTP
        data = response.json()  #convertit json en dictionnaire 
    except requests.RequestException as e:
        log.error(f"Erreur page {page} : {e}")
        break


    #print(response.status_code==200)
    #print(response.text[:500])

    #print(type(données))
    #print(len(données))

    games = list(data.values())
    all_games.extend(games)
    log.info(f"→ {len(games)} jeux récupérés (total : {len(all_games)})")
    
    if page < 2:  #pas de pause après la dernière page
        log.info("Pause 60 secondes...")
        time.sleep(60)


timestamp = datetime.now().strftime("%Y%m%d_%H%M") 
file = open(f"data/raw/steamspy_{timestamp}.csv", "w", newline="", encoding="utf-8") 

writer = csv.DictWriter(file, fieldnames=games[0].keys())
writer.writeheader()
writer.writerows(all_games)
file.close();

log.info(f"{len(all_games)} jeux sauvegardés")