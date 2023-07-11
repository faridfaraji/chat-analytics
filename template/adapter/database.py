# TODO: Let's not copy paste! This should be a shared class in a utils library


class Database:
    # instance attribute
    @classmethod
    def __init__(cls, db_base_url):
        cls.db_base_url = db_base_url

    @classmethod
    def _gen_url(cls, route):
        return f"{cls.db_base_url}/{route}"

    @classmethod
    def _make_request(cls, method, route, *args, **kwargs):
        response = method(
            cls._gen_url(route),
            *args,
            **kwargs,
        )
        response.raise_for_status()
        return response.json()
