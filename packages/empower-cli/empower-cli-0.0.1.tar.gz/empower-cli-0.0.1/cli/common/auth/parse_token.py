from .config import keycloak_openid


def get_user_info(token: str) -> dict[str, str]:
    """Parse user info from access token.

    :param token: access token string
    :return: user info dictionary
    """
    user_fields = ("sub", "name", "email", "perferred_username")
    return {
        key: value
        for key, value in keycloak_openid.userinfo(token).items()
        if key in user_fields
    }
