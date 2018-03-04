from django.contrib.auth import authenticate


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    print(username)
    authenticate(remote_user=username)
    return username
