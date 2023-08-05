from django.conf import settings

import httpx


def req(url, method="get", auth=True, **kwargs):
    if auth:
        kwargs["headers"] = {"Authorization": f"Bearer {settings.SYNGO_ACCESS_TOKEN}"}
    return getattr(httpx, method)(f"{settings.SYNGO_MATRIX_URL}{url}", **kwargs)


def register(user):
    # https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html
    # create-or-modify-account
    return req(
        f"/_synapse/admin/v2/users/@{user.username}:{settings.SYNGO_MATRIX_DOMAIN}",
        method="put",
        json={"displayname": str(user)},
    )


def list_accounts(guests=False):
    # https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html
    # list-accounts
    accounts = []
    next_token = 0
    while True:
        ret = req(
            "/_synapse/admin/v2/users",
            params={"from": next_token, "limit": 10, "guests": guests},
        ).json()
        accounts += ret["users"]
        if "next_token" in ret:
            next_token = ret["next_token"]
        else:
            break
    return accounts
