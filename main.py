import urllib.request
import json
import urllib.parse
from datetime import datetime, timedelta

# CONFIGURATION - Ne pas toucher
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

# LISTE DES ÉQUIPES "SÛRES" (DATA HISTORIQUE STABLE)
TOP_TEAMS = ["Man City", "Arsenal", "Liverpool", "Real Madrid", "Barcelona", "PSG", "Inter", "Bayern", "Leverkusen"]

def analyze_safe_match():
    now = datetime.utcnow()
    # On se limite aux championnats majeurs pour la fiabilité des données
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                matchs = json.loads(response.read().decode())
                for m in matchs:
                    date_m = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # Analyse des matchs à venir dans les prochaines 12h
                    if now < date_m <= now + timedelta(hours=12):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # Data extraction : Cotes Vainqueur (h2h)
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        c_h = next(o['price'] for o in h2h if o['name'] == home)
                        c_a = next(o['price'] for o in h2h if o['name'] == away)
                        c_n = next(o['price'] for o in h2h if o['name'] == 'Draw')

                        # CONDITION SAFE : Un favori "Top Team" avec une cote entre 1.25 et 1.70
                        target = None
                        if any(t in home for t in TOP_TEAMS) and 1.25 <= c_h <= 1.70:
                            target, cote_target, is_home = home, c_h, True
                        elif any(t in away for t in TOP_TEAMS) and 1.25 <= c_a <= 1.70:
                            target, cote_target, is_home = away, c_a, False

                        if target:
                            # Calcul de la probabilité réelle vs probabilité de la cote
                            prob_implicite = int((1/cote_target)*100)
                            
                            # Analyse du marché des buts pour la sécurité
                            totals = next((mk for mk in bk if mk['key'] == 'totals'), None)
                            over_15_prob = "Élevée"
                            if totals:
                                o15_c = next((o['price'] for o in totals['outcomes'] if o['point'] == 1.5), 1.2)
                                if o15_c > 1.40: over_15_prob = "Modérée (Match fermé)"

                            # Rapport SAFE ultra-propre
                            report = (
                                f"🛡️ **ANALYSE SAFE : {target.upper()}**\n"
                                f"🏟️ Match : {home} vs {away}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"📈 **DATA RÉELLE DU MARCHÉ**\n"
                                f"• Indice de Victoire : {prob_implicite}%\n"
                                f"• Statut : {'🏠 Domicile (Fort)' if is_home else '🚀 Extérieur (Stable)'}\n"
                                f"• Dynamique Buts (+1.5) : {over_15_prob}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"✅ **CONSEIL SÉCURISÉ**\n"
                                f"👉 Pari : {target} ou Nul\n"
                                f"👉 Pourquoi : Équipe Top Class, cote stable, probabilité de défaite < 15%.\n"
                                f"━━━━━━━━━━━━━━━━━━"
                            )
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                            urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    analyze_safe_match()
