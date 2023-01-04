import requests

from settings import USER_HANDLER, ADAPTERS_HANDLER


def get_user_handler_url():
    return f"{USER_HANDLER[1]}:{USER_HANDLER[2]}"


def get_adapters_handler_url():
    return f"{ADAPTERS_HANDLER[1]}:{ADAPTERS_HANDLER[2]}"


def check_reachability(service_name, service_url):
    try:
        response = requests.get(service_url)
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"Service {service_name} is not reachable.\nError: {e}")
    return True


def is_user_handler_reachable():
    user_handler_url = get_user_handler_url()
    return check_reachability("user_handler", user_handler_url)


def is_adapters_handler_reachable():
    adapters_handler_url = f"{ADAPTERS_HANDLER[1]}:{ADAPTERS_HANDLER[2]}"
    return check_reachability("adapters_handler", adapters_handler_url)
