try:
    import httpx
except ImportError:
    httpx = None
import requests


def make_req():
    return requests.Session()


def make_httpx_tryimport():
    return httpx.Client()


def make2():
    return make_req()
