import requests
import json
import datetime

custom_headers = {
        "User-Agent": "Ameen (ameenstartshackclub@gmail.com)"
    }

def get_page():
    date = str(datetime.datetime.now()).split()[0].split("-")
    year = str(date[0])
    month = str(date[1])
    day = str(date[2])
    page = requests.get(f"https://api.wikimedia.org/feed/v1/wikipedia/en/featured/{year}/{month}/{day}?format=json", headers=custom_headers)
    return page

def choice(page):
    content = page.json()
    title = content["tfa"]["titles"]["normalized"]
    desc = content["tfa"]["extract"]
    pageid = content["tfa"]["pageid"]
    print(f"{title}")
    yn = input("is this good?(y/n/m) ")
    update_profile(title, desc, pageid, yn)
    articles = content["mostread"]["articles"]
    for article in articles:
        title = article["titles"]["normalized"]
        desc = article["extract"]
        pageid = article["pageid"]
        print(f"{title}")
        yn = input("is this good?(y/n/m) ")
        update_profile(title, desc, pageid, yn)
    
def update_profile(title, desc, pageid, yn):
     while True:
             if yn == "m":
                 print(f"{desc} \n {desc}")
                 yn = input("is this good?(y/n) ")
     
             elif yn == "y":
                 paramss = {
                     "action": "query",
                     "format": "json",
                     "prop": "links",
                     "titles": title,
                     "pllimit": "max"
                 }
                 url = f"https://en.wikipedia.org/w/api.php"
                 page = requests.get(url, headers=custom_headers, params=paramss)
                 data = page.json()
     
                 with open("profile.json", "r") as file:
                             profile = json.loads(file.read())
     
                 profile_data = data["query"]["pages"][str(pageid)]["links"]
     
                 for link in profile_data:
                     link = link["title"]
                     if link in profile["user"]["interests"]:
                         no = int(profile["user"]["interests"][link])
                         profile["user"]["interests"][link] = no + 1
                     elif link not in profile:
                         profile["user"]["interests"][link] = 1
                 with open("profile.json", "w") as file:
                     file.write(json.dumps(profile, indent=4))
     
                 break
     
             elif yn == "n":
                 ...
                 break
             else: yn = input("is this good?(y/n/m) ")
     

def main():
     page = get_page()
     choice(page)

if __name__ == "__main__":
    main()