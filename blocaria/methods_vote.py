import requests

# URL de l'API
login_url = "https://voteapi.rivrs.io/v1/user/login"
data_url = "https://voteapi.rivrs.io/v1/vote/availableVote"
uptime_url = "https://api.uptimerobot.com/v2/getMonitors"


def get_roles_status(login_data):
    # Informations pour la requête POST de login
    headers = {"Content-Type": "text/plain", "Origin": "https://blocaria.fr"}

    # Faire la requête POST pour se connecter
    login_response = requests.post(login_url, data=login_data, headers=headers)

    # Vérifiez si la connexion a réussi
    if login_response.status_code == 200:
        # Si la connexion réussit, récupérez les cookies de session
        cookies = login_response.cookies

        # Utiliser les cookies pour faire la requête GET authentifiée
        response = requests.get(data_url, cookies=cookies)

        if response.status_code == 200:
            available_vote_data = response.json()
        else:
            available_vote_data = {
                "error": "Failed to retrieve data from API."
            }
    else:
        available_vote_data = {"error": "Login failed."}

    return available_vote_data
