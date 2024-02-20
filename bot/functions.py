import requests
import logging
import hashlib
import random


def create_user(username, data_limit, expire, access_token, api_url):
    url = f"{api_url}/api/user"

    payload = {
        "username": username,
        "proxies": {
            "vmess": {},
            "vless": {}
        },
        "inbounds": {
            "vmess": [],
            "vless": []
        },
        "expire": expire,
        "data_limit": data_limit * 1024 ** 3,
        "data_limit_reset_strategy": "no_reset",
        "status": "active",
        "note": "",
        "on_hold_timeout": "2023-11-03T20:30:00",
        "on_hold_expire_duration": 0
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while creating user {username}: {e}")
        return None


logging.basicConfig(filename='script_log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def get_access_token(username, password, api_url):
    url = f"{api_url}/api/admin/token"
    data = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while obtaining access token: {e}')
        return None

def generate_custom_id(length):
    random_number = str(random.getrandbits(256))  # Generate a random 256-bit number
    hashed = hashlib.sha256(random_number.encode()).hexdigest()  # Hash the random number
    return hashed[:length]  # Return the first `length` characters

def get_user(username, access_token, api_url):
    url = f"{api_url}/api/user/{username}"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while getting user {username}: {e}")
        return None


