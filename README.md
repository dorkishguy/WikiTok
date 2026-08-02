# WikiTok
 
a streamlit app that learns what you're into on wikipedia and starts recommending you shit based on it. swipe yes/no on articles like it's tinder for knowledge.
 
## how it works
 
1. shows you a wikipedia article (title, image, extract)
2. you hit **yes** or **no**
3. on yes, it pulls all the internal wiki links from that article and bumps a counter for each one in `profile.json`
4. once a link's counter crosses a threshold, it becomes a "candidate" — next time `recc()` runs, it fetches that page's summary and shows it to you as a recommendation
5. repeat forever, profile gets sharper over time
basically: click yes on an article → app learns what topics are adjacent to your interests → starts feeding you those.
 
## setup
 
```bash
pip install streamlit requests
streamlit run wikipedia.py
```
 
first run auto-creates `profile.json` with an empty interests/shown structure. no other config needed.
 
## file structure
 
- `app.py` — the whole app, single file
- `profile.json` — local state, gets created on first run
  - `user.interests` — dict of `{topic: score}`, candidates waiting to be recommended
  - `user.shown` — topics already shown, moved out of `interests` so they don't repeat
