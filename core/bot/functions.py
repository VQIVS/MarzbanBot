import requests
import logging
import hashlib
import random
from uuid import uuid4


def create_user(username, data_limit, expire, access_token, api_url):
    """
    Create a new user with the provided parameters.

    Args:
        username (str): The username of the new user.
        data_limit (float): The data limit for the new user.
        expire (int): The expiration date for the new user.
        access_token (str): The access token for API authentication.
        api_url (str): The URL of the API endpoint.

    Returns:
        dict: The response JSON containing user information if successful, None otherwise.
    """
    url = f"{api_url}/api/user"

    # Calculate on_hold_expire_duration based on the expire parameter

    payload = {
        "username": username,
        "proxies": {"vmess": {}, "vless": {}},
        "inbounds": {"vmess": [], "vless": []},
        "expire": None,
        "data_limit": data_limit * 1024**3,
        "data_limit_reset_strategy": "no_reset",
        "status": "on_hold",
        "note": "",
        "on_hold_expire_duration": expire,
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while creating user {username}: {e}")
        return None


def get_access_token(username, password, api_url):
    """
    Obtain the access token for API authentication.

    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.
        api_url (str): The URL of the API endpoint.

    Returns:
        str: The access token if successful, None otherwise.
    """
    url = f"{api_url}/api/admin/token"
    data = {"username": username, "password": password}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()["access_token"]
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while obtaining access token: {e}")
        return None


def generate_custom_id(length):
    """
    Generate a custom ID with the specified length.

    Args:
        length (int): The length of the custom ID.

    Returns:
        str: The generated custom ID.
    """
    random_number = str(random.getrandbits(256))  # Generate a random 256-bit number
    hashed = hashlib.sha256(
        random_number.encode()
    ).hexdigest()  # Hash the random number
    return hashed[:length]  # Return the first `length` characters


def get_user(username, access_token, api_url):
    """
    Get user information for the specified username.

    Args:
        username (str): The username of the user to retrieve information for.
        access_token (str): The access token for API authentication.
        api_url (str): The URL of the API endpoint.

    Returns:
        dict: The response JSON containing user information if successful, None otherwise.
    """
    url = f"{api_url}/api/user/{username}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while getting user {username}: {e}")
        return None


def modify_user(username, expire, data_limit, access_token, api_url):
    """
    Modify an existing user's details in the API.

    Parameters:
        username (str): The username of the user to modify.
        expire (str): The expiration date of the user's subscription.
        data_limit (float): The data limit for the user's subscription.
        access_token (str): The access token for authentication.
        api_url (str): The URL of the API.

    Returns:
        dict or None: The JSON response from the API if successful, otherwise None.
    """
    url = f"{api_url}/api/user/{username}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "username": username,
        "proxies": {"vmess": {}, "vless": {}},
        "inbounds": {"vmess": [], "vless": []},
        "expire": expire,
        "data_limit": data_limit * 1024**3,
        "data_limit_reset_strategy": "no_reset",
        "status": "active",
        "note": "",
        "on_hold_timeout": "2023-11-03T20:30:00",
        "on_hold_expire_duration": 0,
    }
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while modifying user {username}: {e}")
        return None


def reset_user_usage(username, access_token, api_url):
    """
    Reset the usage statistics for a specific user.

    Parameters:
        username (str): The username of the user to reset usage.
        access_token (str): The access token for authentication.
        api_url (str): The URL of the API.

    Returns:
        dict or None: The JSON response from the API if successful, otherwise None.
    """
    url = f"{api_url}/api/user/{username}/reset"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while resetting user {username}'s usage: {e}")
        return None


def delete_user(username, access_token, api_url):
    """
    Deletes a user with the specified username.

    Args:
        username (str): The username of the user to delete.
        access_token (str): The access token for authentication.
        api_url (str): The URL of the API.

    Returns:
        dict or None: A dictionary containing the response data if successful, otherwise None.

    """
    url = f"{api_url}/api/user/{username}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while resetting user {username}'s usage: {e}")
        return None


def generate_referral_link(user_id, bot_url):
    code = str(uuid4())
    link = f'{bot_url}?start={code}'
    return link