class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class AdminModel:
    pass


class AdminSite:

    def __init__(self):
        self._registry = {}

    def register(self):
        pass

    def get_registry(self):
        return self._registry

    def get_urls(self):
        pass
