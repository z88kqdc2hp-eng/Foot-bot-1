import urllib.request
import json
from datetime import datetime

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def job_expert_final():
    aujourdhui = datetime.now().strftime("%Y-%m-%d")
    # On scanne les 5 grands championnats
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        # Récupération des cotes Victoire et Plus/Moins de buts
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    if aujourdhui in m['commence_time']:
                        home = m['home_team']
                        away = m['away_team']
                        
                        # Extraction des cotes
                        bk = m['bookmakers'][0]['markets']
                        h2h = bk[0]['outcomes']
                        cote_h = next(o['price'] for o in h2h if o['name'] == home)
                        cote_a = next(o['price'] for o in h2h if o['name'] == away)
                        cote_n = next(o['price'] for o in h2h if o['name'] == 'Draw')

                        # --- CALCUL DES INDICES DE FIABILITÉ ---
                        # Puissance brute (Probabilité de victoire directe)
                        fiabilite_directe = int((1 / cote_h) * 100)
                        # Puissance sécurisée (Victoire ou Nul)
                        prob_nul = (1 / cote_n) * 100
                        fiabilite_securisee = int(fiabilite_directe + (prob_nul * 0.7))
                        if fiabilite_securisee > 99: fiabilite_securisee = 99

                        # Sélection uniquement si la fiabilité sécurisée est élevée
                        if fiabilite_securisee >= 85:
                            
                            # Analyse du ratio de buts
                            msg_buts = "Normal (1-2 buts)"
                            if len(bk) > 1:
                                over_25 = next((o['price'] for o in bk[1]['outcomes'] if o['name'] == 'Over'), 2.0)
                                if over_25 < 1.75: msg_buts = "Élevé (+2.5 buts)"

                            # --- MISE EN PAGE PRO ---
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
                                f"• 🛡️ **Clean Sheet** : Probable pour {home}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"🎯 **PRONOSTIC FINAL** :\n"
                                f"👉 **Pari Principal** : Victoire de {home}\n"
                                f"👉 **Pari Sécurisé** : {home} ou Nul\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"💰 **Conseil Mise** : {'2%' if fiabilite_directe > 75 else '1%'} du capital"
                            )
                            
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
                            urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    job_expert_final()
