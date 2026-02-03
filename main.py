import urllib.request
import urllib.parse

# Tes identifiants
TOKEN = "8341397638:AAENHUF8V4FoCenp9aR7ockDcHAGZgmN66s"
ID = "1697906576"

def test_telegram():
    msg = "🚀 TEST RÉUSSI : La connexion entre GitHub et ton Telegram est parfaite !"
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}"
    try:
        urllib.request.urlopen(api_url)
        print("Message envoyé avec succès !")
    except Exception as e:
        print(f"Erreur technique : {e}")

if __name__ == "__main__":
    test_telegram()
