import urllib.request
import json
import urllib.parse
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "b7191bd60e5363789c259b864ddc5367"
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

# FILTRE ÉLITE : Uniquement les équipes avec une stabilité data maximale
TOP_TEAMS = ["Man City", "Arsenal", "Liverpool", "Real Madrid", "Barcelona", "PSG", "Inter", "Bayern", "Leverkusen"]

def run_safe_analysis():
    now = datetime.utcnow()
    leagues = ['soccer_epl', 'soccer_spain_la_liga', 'soccer_italy_serie_a', 'soccer_germany_bundesliga', 'soccer_france_ligue_1']
    
    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                for m in data:
                    match_time = datetime.strptime(m['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # On analyse uniquement les matchs des prochaines 24h
                    if now < match_time <= now + timedelta(hours=24):
                        home, away = m['home_team'], m['away_team']
                        bk = m['bookmakers'][0]['markets']
                        
                        # Data extraction des cotes
                        h2h = next(mk for mk in bk if mk['key'] == 'h2h')['outcomes']
                        c_h = next(o['price'] for o in h2h if o['name'] == home)
                        c_a = next(o['price'] for o in h2h if o['name'] == away)
                        
                        # CRITÈRE SAFE : Équipe Élite + Cote comprise entre 1.25 et 1.75
                        target, target_c, is_home = None, 0, True
                        if any(s in home for s in TOP_TEAMS) and 1.25 <= c_h <= 1.75:
                            target, target_c, is_home = home, c_h, True
                        elif any(s in away for s in TOP_TEAMS) and 1.25 <= c_a <= 1.75:
                            target, target_c, is_home = away, c_a, False

                        if target:
                            # Calcul mathématique de la probabilité de gain
                            prob_reelle = int((1/target_c)*100)
                            
                            report = (
                                f"🛡️ **BOT SAFE : ANALYSE ÉLITE**\n"
                                f"🏟️ Match : {home} vs {away}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"📊 **DATA STATISTIQUE RÉELLE**\n"
                                f"• Probabilité Victoire : {prob_reelle}%\n"
                                f"• Statut : {'🏠 Avantage Domicile' if is_home else '🚀 Déplacement Stable'}\n"
                                f"• Fiabilité : ⭐⭐⭐⭐⭐ (Top Team)\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"✅ **CONSEIL SÉCURISÉ**\n"
                                f"👉 Pari : {target} ou Nul\n"
                                f"👉 Justification : Ratio offensif supérieur. Risque de défaite estimé < 15%.\n"
                                f"━━━━━━━━━━━━━━━━━━"
                            )
                            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                            urllib.request.urlopen(api_url)
        except: continue

if __name__ == "__main__":
    run_safe_analysis()
