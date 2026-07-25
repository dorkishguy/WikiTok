import json

with open("pagejson.json", "r") as file:
    data = json.loads(file.read())

articles = data["mostread"]["articles"]

for article in articles:
    print(article["titles"]["normalized"])