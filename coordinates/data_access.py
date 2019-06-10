import json
import requests

COORDINATES_URL = "https://damp-ocean-98658.herokuapp.com/api/v1/user/complain/coordinates"
AUTH_URL = "https://auth-service-huachicol.herokuapp.com/oauth/token"


def _authenticate():
    payload = "username=fer%40gmail.com&password=12345&grant_type=password&undefined="
    h = {
        'Authorization': "Basic YW5ndWxhcmp3dGNsaWVudGlkOjEyMzQ1",
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    r = requests.post(
        url=AUTH_URL,
        data=payload,
        headers=h
    )

    data = r.json()
    with open('token', 'w') as f:
        f.write(data['access_token'])

    return data


def get_coordinates():
    coordinate_headers = {
        'cache-control': "no-cache",
        'Content-Type': "application/json",
    }
    try:
        # Token exists directory
        with open('token') as f:
            print('Se utilizara token obtenido de la sesion pasada.')
            access_token = f.read()

    except FileNotFoundError:
        # No token. Request a new one.
        print('Aun no se cuenta con token. Se solicitara uno.')
        auth = _authenticate()
        access_token = auth['access_token']

    # Fetch coordinates
    coordinate_headers['Authorization'] = 'Bearer ' + access_token
    h = {
        'Authorization': 'Bearer ' + access_token,
        'cache-control': "no-cache",
        'Content-Type': "application/json",
    }
    resp = requests.get(
        url=COORDINATES_URL,
        headers=h
    )
    if resp.status_code == 401:
        print('Token expirado. Solicitando uno nuevo.')
        auth = _authenticate()
        access_token = auth['access_token']

        h = {
            'Authorization': 'Bearer ' + access_token,
            'cache-control': "no-cache",
            'Content-Type': "application/json",
        }

        resp = requests.get(
            url=COORDINATES_URL,
            headers=h
        )

    if resp.status_code != 200:
        raise Exception('No se puede obtener las coordenadas del servicio')

    return resp.json()
