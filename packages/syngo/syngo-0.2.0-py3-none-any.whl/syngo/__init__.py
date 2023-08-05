from datetime import datetime, timedelta

from django.conf import settings

import httpx


def req(url, method="get", auth=True, **kwargs):
    if auth:
        kwargs["headers"] = {"Authorization": f"Bearer {settings.SYNGO_ACCESS_TOKEN}"}
    return getattr(httpx, method)(f"{settings.SYNGO_MATRIX_URL}{url}", **kwargs)


def django_to_matrix(user):
    """Get the matrix id associated to a django user."""
    return f"@{user.username}:{settings.SYNGO_MATRIX_DOMAIN}"


def register(django_user):
    """Register a Django user into a Matrix homeserver."""
    # https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html
    # create-or-modify-account
    user_id = django_to_matrix(django_user)
    return req(
        f"/_synapse/admin/v2/users/{user_id}",
        method="put",
        json={"displayname": str(django_user)},
    )


def list_accounts(guests=False):
    """List accounts on a Matrix homeserver."""
    # https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html
    # list-accounts
    accounts = []
    next_token = 0
    while True:
        ret = req(
            "/_synapse/admin/v2/users",
            params={"from": next_token, "limit": 10, "guests": guests},
        ).json()
        if "users" not in ret:  # pragma: no cover
            raise ValueError(f"Invalid response: {ret}")
        accounts += ret["users"]
        if "next_token" in ret:
            next_token = ret["next_token"]
        else:
            break
    return accounts


def shadow_ban(django_user, unban=False):
    """Shadow-(un)ban an user."""
    # https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html
    # controlling-whether-a-user-is-shadow-banned
    user_id = django_to_matrix(django_user)
    return req(
        f"/_synapse/admin/v1/users/{user_id}/shadow_ban",
        method="delete" if unban else "post",
    )


def deactivate(django_user):
    """Deactivate an account."""
    # https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html
    # deactivate-account
    user_id = django_to_matrix(django_user)
    return req(
        f"/_synapse/admin/v1/deactivate/{user_id}", method="post", json={"erase": True}
    )


def registration_token():
    """Create a registration token."""
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = int(tomorrow.timestamp() * 1000)

    return req(
        "/_synapse/admin/v1/registration_tokens/new",
        method="post",
        json={"uses_allowed": 1, "expiry_time": tomorrow},
    )
