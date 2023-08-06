import lnschema_core


def environment() -> str:
    """Pipeline: 9 base62.

    Collision probability is low for 10M pipelines: 1M users with 10 pipelines/user.
    """
    return lnschema_core.id.base62(n_char=9)
