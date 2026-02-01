import urllib.request
import json
from datetime import datetime

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def job_final_complet():
    aujourdhui = datetime.now().strftime("%Y-%m-%d")
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    if aujourdhui in m['commence_time']:
                        home = m['home_team']
                        away = m['away_team']
                        
                        bk = m['bookmakers'][0]['markets']
                        h2h = bk[0]['outcomes']
                        cote_h = next(o['price'] for o in h2h if o['name'] == home)
                        cote_a = next(o['price'] for o in h2h if o['name'] == away)
                        cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')

                        # CALCULS DES INDICES
                        prob_v = (1 / cote_h) * 100
                        prob_n = (1 / cote_n) * 100
                        
                        fiabilite_directe = int(prob_v)
                        fiabilite_securisee = int(prob_v + (prob_n * 0.8))
                        if fiabilite_securisee > 99: fiabilite_securisee = 99

                        # SEUIL AJUSTÉ À 75% : Pour avoir plus de matchs (comme Tottenham ou Villa)
                        if fiabilite_securisee >= 75:
                            
                            msg_buts = "Normal (1-2 buts)"
                            if len(bk) > 1:
                                over_25 = next((o['price'] for o in bk[1]['outcomes'] if o['name'] == 'Over'), 2.0)
                                if over_25 < 1.80: msg_buts = "Élevé (+2.5 buts)"

                            msg = (
                                f"🛰️ **SCANNER DATA PRO : {home.upper()}**\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"🏟️ **Match** : {home} vs {away}\n"
                                f"📈 **Cote** : {cote_h} | **Nul** : {cote_n}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"🛡️ **INDICES DE CONFIANCE** :\n"
                                f"• ✅ **Victoire Directe** : {fiabilite_directe}%\n"
                                f"• 🛡️ **Sécurité (V ou N)** : {fiabilite_securisee}%\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"📊 **ANALYSE DES RATIOS** :\n"
                                f"• ⚽ **Ratio Buts/Match** : {msg_buts}\n"
                                f"• 🛡️ **Clean Sheet** : {'Possible' if fiabilite_directe > 65 else 'Risqué'}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"🎯 **PRONOSTIC FINAL** :\n"
                                f"👉 **Pari Principal** : Victoire de {home}\n"
                                f"👉 **Pari Sécurisé** : {home} ou Nul\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"💰 **Mise** : {'2%' if fiabilite_directe > 70 else '1%'} du capital"
                            )
                            
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
                            urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    job_final_complet()
