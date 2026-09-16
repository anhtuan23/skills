import logging


def load_profile(client, user_id):
    try:
        payload = client.fetch_profile(user_id)
    except client.NetworkError as exc:
        logging.warning("profile service unavailable: %s", exc)
        return None

    if payload is None:
        return None

    return normalize_profile(payload)
