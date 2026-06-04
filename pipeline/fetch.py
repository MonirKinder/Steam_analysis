import requests 
import csv
url = "https://steamspy.com/api.php"


parametres={
    "request": "all",
    "page": 0}

response = requests.get(url, params=parametres)
print(response.status_code==200)

##print(response.text[:500])

données = response.json()  #convertit json en dictionnaire 
print(type(données))
print(len(données))

premier_jeu = list(données.values())[0]
print(premier_jeu)