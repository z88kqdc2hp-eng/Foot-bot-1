import urllib.request
import json
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def job_final_scouting():
    # Heure actuelle pour filtrer les matchs en cours
    maintenant = datetime.utcnow()
    aujourdhui = maintenant.strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    matchs_valides = []

    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    # FILTRE ANTI-LIVE : On ignore si le match a commencé
                    date_match = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    if date_match < maintenant: continue
                    if aujourdhui not in m['commence_time']: continue
                    
                    home, away = m['home_team'], m['away_team']
                    bk = m['bookmakers'][0]['markets']
                    h2h = bk[0]['outcomes']
                    cote_h = next(o['price'] for o in h2h if o['name'] == home)
                    cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')

                    prob_v = (1 / cote_h) * 100
                    prob_n = (1 / cote_n) * 100
                    fiabilite_s = int(prob_v + (prob_n * 0.8))

                    # On garde les matchs pour l'analyse
                    matchs_valides.append({
                        'home': home, 'away': away, 'cote': cote_h, 
                        'fiabilite': fiabilite_s, 'league': league, 'bk': bk
                    })

                    # Envoi des analyses individuelles habituelles
                    if fiabilite_s >= 75:
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

    # ANALYSE DU MATCH RISQUÉ (CHOISI AU HASARD PARMI LES GROS)
    if matchs_valides:
        # On prend un match avec une cote entre 1.80 et 2.50 (Match serré/risqué)
        choc = next((x for x in matchs_valides if 1.80 <= x['cote'] <= 2.60), matchs_valides[0])
        
        h, a = choc['home'], choc['away']
        analyse_poussee = (
            f"🎯 **L'ANALYSE RISQUÉE DU JOUR : {h} vs {a}**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔥 **Minutes de Buts** : Probabilité forte 15-30' / 75-90'\n"
            f"⚽ **Total Buts** : Plus de 2.5 (Match très ouvert)\n"
            f"🎯 **Buteurs** : Attaquants de pointe des deux clubs\n"
            f"🚩 **Penalty** : Probabilité élevée (Jeu dans la surface)\n"
            f"🛡️ **Clean Sheet** : Impossible (Les deux marquent)\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ **Conseil** : Jouer 'Les deux équipes marquent'"
        )
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(analyse_poussee)}&parse_mode=Markdown")

if __name__ == "__main__":
    job_final_scouting()
