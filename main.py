import urllib.request
import json
from datetime import datetime

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def run_analysis():
    date_today = datetime.now().strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                for m in data:
                    if date_today in m['commence_time']:
                        home = m['home_team']
                        cote = m['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
                        # Filtre Stars Elite
                        stars = ["City", "Real", "Barca", "Bayern", "Arsenal", "Liverpool", "Inter"]
                        if any(s in home for s in stars) and 1.30 <= cote <= 1.90:
                            msg = f"🏆 **PRONO SAFE**\n\n⚽ {home}\n📈 Cote : {cote}\n✅ Verdict : Fiable"
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
                            urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    run_analysis()
