import requests

from utilities import get_user_handler_url, get_adapters_handler_url


def check_auth(authorization, user_handler_url=get_user_handler_url()):
    """
    Check if the user is authorized to access the API.
    """
    access_token = authorization.replace("Bearer ", "")

    url = f"{user_handler_url}/check_token"
    payload = {"access_token": access_token}
    response = requests.post(url, json=payload)
    return response.json()


def create_short_url(user_id, url, alias, note, preferred_service, adapters_handler_url=get_adapters_handler_url()):
    """
    Create a short URL.
    """
    create_url = f"{adapters_handler_url}/create_short_url"
    payload = {
        "user_id": user_id,
        "url": url,
        "alias": alias,
        "note": note,
        "preferred_service": preferred_service,
    }
    response = requests.post(create_url, json=payload)
    return response.json()


def delete_short_url(user_id, short_url_id, adapters_handler_url=get_adapters_handler_url()):
    """
    Delete a short URL.
    """
    delete_url = f"{adapters_handler_url}/delete_short_url"
    payload = {
        "user_id": user_id,
        "short_url_id": short_url_id,
    }
    response = requests.delete(delete_url, params=payload)
    return response.json()
