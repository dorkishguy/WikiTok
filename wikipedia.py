import requests
import json
import datetime
import streamlit as st
from pathlib import Path

custom_headers = {
        "User-Agent": "Ameen (ameenstartshackclub@gmail.com)"
    }

main_container = st.empty()

st.header("Future of wikipedia cuz everyone is losing their attention spans :/")

path = Path("profile.json")

if not path.is_file():
     with open("profile.json", "w") as file:
          template = {"user": {"interests": {}, "shown": {}}}
          file.write(json.dumps(template, indent=4))

def choice():
    date = str(datetime.datetime.now() - datetime.timedelta(days=1)).split()[0].split("-")
    year = str(date[0])
    month = str(date[1])
    day = str(date[2])
    if "articles" not in st.session_state:
        page = requests.get(f"https://api.wikimedia.org/feed/v1/wikipedia/en/featured/{year}/{month}/{day}?format=json", headers=custom_headers)
        try:
            content = page.json()
        except requests.exceptions.JSONDecodeError:
            st.write("something went wrong")
        tfa = content["tfa"]
        mostread = content["mostread"]["articles"]
        st.session_state.articles = [tfa] + mostread
        st.session_state.idx = 0
    articles = st.session_state.articles
    idx = st.session_state.idx
    if idx < len(articles):
        a = articles[idx]
        title = a["titles"]["normalized"]
        desc = a["extract"]
        pageid = a["pageid"]
        image = a.get("thumbnail", {}).get("source")
        streamlit(image, title, desc, pageid)
    else:
        recc()
    

def streamlit(image, title, desc, pageid):
    with main_container.container():
            if image != None:
                st.image(str(image))
            st.write(title)
            st.write(desc)
            y = False
            n = False
            col1, col2 = st.columns([1,1])
            with col1:
                if st.button('yes', key = f"y{pageid}"):
                     y = True
            with col2:
                if st.button('no', key = f"n{pageid}"):
                     n = True
                     
            if y:
                update_profile(title, pageid, "y")
                st.session_state.idx += 1
                st.rerun()
            if n:
                update_profile(title, pageid, "n")
                st.session_state.idx += 1
                st.rerun()
    
def update_profile(title, pageid, yn):
        if yn == "y":
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
                elif link not in profile["user"]["interests"]:
                    profile["user"]["interests"][link] = 1

            profile["user"]["interests"] = {k: v for k, v in sorted(profile["user"]["interests"].items(), key=lambda item: item[1], reverse=True)}
            
            with open("profile.json", "w") as file:
                file.write(json.dumps(profile, indent=4))
    
        elif yn == "n":
            ...
        else:
            pass

def update_shown(title):
    with open("profile.json", "r") as file:
        profile = json.loads(file.read())
    title = list(profile["user"]["interests"].items())[0][0]
    print(title)
    value = profile["user"]["interests"].pop(title)
    profile["user"]["shown"][title] = value
    with open("profile.json", "w") as file:
        file.write(json.dumps(profile, indent=4))
        

def recc():
    with open("profile.json", "r") as file:
        profile = json.loads(file.read())
    for interest, value in profile["user"]["interests"].items():
        if value > 1:
            interest = interest.replace(" ", "_")
            page = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{interest}", headers=custom_headers)
            if page.status_code == 404:
                continue
            page = page.json()
            title = page["titles"]["normalized"]
            desc = page["extract"]
            pageid = page["pageid"]
            try:
                image = page["thumbnail"].get("source")
            except KeyError:
                 image = None
            streamlit(image, title, desc, pageid)
            update_shown(title)
            return
             



def main():
    choice()

if __name__ == "__main__":
    main()
