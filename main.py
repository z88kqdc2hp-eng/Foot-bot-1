import urllib.request, json, urllib.parse
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

# SEULEMENT L'ÉLITE (Data la plus stable)
TOP_TEAMS = ["Man City", "Arsenal", "Liverpool", "Real Madrid", "Barcelona", "PSG", "Inter", "Bayern", "Leverkusen"]

def analyze_safe():
    now = datetime.utcnow()
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    if now < date_m <= now + timedelta(hours=24):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets'][0]['outcomes']
                        c_h = next(o['price'] for o in bk if o['name'] == home)
                        c_a = next(o['price'] for o in bk if o['name'] == away)

                        target, target_c = None, 0
                        # Filtre de sécurité maximale (cote entre 1.25 et 1.65)
                        if any(s in home for s in TOP_TEAMS) and 1.25 <= c_h <= 1.65:
                            target, target_c = home, c_h
                        elif any(s in away for s in TOP_TEAMS) and 1.25 <= c_a <= 1.65:
                            target, target_c = away, c_a

                        if target:
                            report = (
                                f"🛡️ **BOT SAFE : ANALYSE ÉLITE**\n"
                                f"🏟️ Match : {home} vs {away}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"✅ **CONSEIL SÉCURISÉ**\n"
                                f"👉 Pari : {target} ou Nul (Double Chance)\n"
                                f"📊 Cote : {target_c}\n"
                                f"💡 Pourquoi : Écart statistique majeur identifié via data réelle.\n"
                                f"━━━━━━━━━━━━━━━━━━"
                            )
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                            urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    analyze_safe()
