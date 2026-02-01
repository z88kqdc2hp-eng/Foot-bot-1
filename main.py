import urllib.request
import json
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def job_final_ultra():
    maintenant = datetime.utcnow()
    aujourdhui = maintenant.strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    selection_combine = []
    match_choc = None
    ecart_minimal = 100

    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    # 1. FILTRE TEMPS RÉEL : On ignore les matchs commencés
                    date_match = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    if date_match < maintenant + timedelta(minutes=15): continue
                    
                    home, away = m['home_team'], m['away_team']
                    bk = m['bookmakers'][0]['markets']
                    h2h = bk[0]['outcomes']
                    cote_h = next(o['price'] for o in h2h if o['name'] == home)
                    cote_a = next(o['price'] for o in h2h if o['name'] == away)
                    cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')

                    prob_v = (1 / cote_h) * 100
                    prob_n = (1 / cote_n) * 100
                    fiabilite_s = int(prob_v + (prob_n * 0.8))

                    # 2. DÉTECTION DU CHOC (Match le plus serré)
                    diff = abs(cote_h - cote_a)
                    if diff < ecart_minimal:
                        ecart_minimal = diff
                        match_choc = m

                    # 3. ANALYSE DES MATCHS INDIVIDUELS (Seuil 75%)
                    if fiabilite_s >= 75:
                        # Ajout au combiné si la cote est "joueuse" (entre 1.40 et 1.75)
                        if 1.40 <= cote_h <= 1.75:
                            selection_combine.append(f"{home} (V ou N)")

                        msg = (
                            f"🛰️ **SCANNER DATA : {home.upper()}**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🏟️ **Match** : {home} vs {away}\n"
                            f"🛡️ **Sécurité (V ou N)** : {fiabilite_s}%\n"
                            f"👉 **Pari** : Victoire de {home}\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except: continue

    # 4. ANALYSE DÉTAILLÉE DU CHOC
    if match_choc:
        h, a = match_choc['home_team'], match_choc['away_team']
        choc_msg = (
            f"🔥 **L'ANALYSE DU CHOC : {h} vs {a}** 🔥\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📝 **CONTEXTE** : Match à haute intensité.\n"
            f"💡 **LE BON COUP** : 'Les deux équipes marquent'.\n"
            f"🎯 **BUTEUR PROBABLE** : La star offensive du club à domicile.\n"
            f"🛡️ **CLEAN SHEET** : Très peu probable (Match ouvert).\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ **CONSEIL** : Jouer le 'Plus de 1.5 buts' pour sécuriser."
        )
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(choc_msg)}&parse_mode=Markdown")

    # 5. LE COMBINÉ "JOUEUR" (Cotes plus intéressantes)
    if len(selection_combine) >= 2:
        ticket = "💰 **COMBINÉ JOUEUR (COTE BOOSTÉE)**\n\n"
        ticket += " 🚀 " + " + ".join(selection_combine[:2])
        ticket += "\n\n🎯 **Objectif** : Doubler la mise en sécurité."
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(ticket)}&parse_mode=Markdown")

if __name__ == "__main__":
    job_final_ultra()
