from urllib.request import getproxies


def get_local_proxy():
    try:
        return getproxies()['http']
    except KeyError:
        return None
