import urllib.request
import json
from datetime import datetime

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def job_ultime():
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
                    # FILTRE ANTI-LIVE & DATE
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    if date_m < maintenant or aujourdhui not in m['commence_time']: continue
                    
                    home, away = m['home_team'], m['away_team']
                    bk = m['bookmakers'][0]['markets']
                    h2h = bk[0]['outcomes']
                    cote_h = next(o['price'] for o in h2h if o['name'] == home)
                    cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')

                    # CALCULS DE FIABILITÉ CLAIRS
                    prob_v = int((1 / cote_h) * 100)
                    prob_n = int((1 / cote_n) * 100)
                    fiab_securisee = int(prob_v + (prob_n * 0.8))
                    if fiab_securisee > 99: fiab_securisee = 99

                    # ANALYSE DU NOMBRE DE BUTS (OVER 2.5)
                    tendance_buts = "Moins de 2.5 (Match fermé)"
                    if len(bk) > 1:
                        over_25 = next((o['price'] for o in bk[1]['outcomes'] if o['name'] == 'Over'), 2.0)
                        if over_25 < 1.75: tendance_buts = "Plus de 2.5 (Match offensif)"

                    matchs_valides.append({'h': home, 'a': away, 'cote': cote_h, 'fiab': prob_v})

                    # ENVOI ANALYSE STANDARD
                    if fiab_securisee >= 75:
                        msg = (
                            f"🛰️ **ANALYSE DATA : {home.upper()}**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🏟️ **Match** : {home} vs {away}\n"
                            f"📊 **Fiabilité Victoire** : {prob_v}%\n"
                            f"🛡️ **Fiabilité Victoire/Nul** : {fiab_securisee}%\n"
                            f"⚽ **Nombre de buts** : {tendance_buts}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 **MON CONSEIL** :\n"
                            f"👉 Pari conseillé : **{home} ou Nul**\n"
                            f"👉 Pari risqué : **Victoire de {home}**\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
                        urllib.request.urlopen(api_url)
        except: continue

    # MODULE PARI RISQUÉ DU JOUR
    if matchs_valides:
        # On choisit un match avec une cote intéressante (entre 1.8 et 2.6)
        choc = next((x for x in matchs_valides if 1.8 <= x['cote'] <= 2.6), matchs_valides[0])
        h, a = choc['h'], choc['a']
        analyse_choc = (
            f"🔥 **LE PARI RISQUÉ DU JOUR : {h} vs {a}**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⚽ **Buts** : Plus de 2.5 attendus\n"
            f"🎯 **Buteurs** : Fortes chances pour l'attaquant de {h}\n"
            f"🚩 **Penalty** : Probabilité élevée dans ce match\n"
            f"⏱️ **Minute de but** : 1er but avant la 30ème min\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ **CONSEIL** : Les deux équipes marquent"
        )
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(analyse_choc)}&parse_mode=Markdown")

if __name__ == "__main__":
    job_ultime()
