import requests 
import csv
import time

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
        print(f"Error fetching data: {e}")
        break


    #print(response.status_code==200)
    #print(response.text[:500])

    #print(type(données))
    #print(len(données))

    games = list(data.values())
    all_games.extend(games)
    print(f"  → {len(games)} jeux récupérés (total : {len(all_games)})")
    
    print("Pause 60 secondes...")
    time.sleep(60)

   
file = open("data/raw/steamspy_3pages.csv", "w", newline="", encoding="utf-8") 

writer = csv.DictWriter(file, fieldnames=games[0].keys())
writer.writeheader()
writer.writerows(all_games)
file.close();

print(f"{len(all_games)} jeux sauvegardés")