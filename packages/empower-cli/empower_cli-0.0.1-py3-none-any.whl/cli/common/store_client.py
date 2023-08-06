import pickledb


# add top level store container (dictionary) names here to be used as 'string constants'
class StoreContainers:
    environment = "environment"
    user = "user"


container_names = StoreContainers()


class Store:
    """Client class for working with the data store."""

    def __init__(self):
        self._db = pickledb.load(".store.db", False)
        self._initialize_dict(container_names.environment)
        self._initialize_dict(container_names.user)

    def get_all(self, container_name):
        return self._db.dgetall(container_name)

    def save(self, container_name: str, **kwargs):
        """
        Save a set of key value pair arguments
        """
        for key, value in kwargs:
            self._set(container_name, key, value)

    @property
    def empower_api_url(self) -> str:
        return self._db.get(container_names.environment).get("empower_api_url")

    @empower_api_url.setter
    def empower_api_url(self, value: str) -> None:
        # todo: add yield error handling
        self._set(container_names.environment, "empower_api_url", value)

    @property
    def empower_discovery_url(self) -> str:
        return self._db.get(container_names.environment).get("empower_discovery_url")

    @empower_discovery_url.setter
    def empower_discovery_url(self, value: str) -> None:
        self._set(container_names.environment, "empower_discovery_url", value)

    @property
    def empower_licensing_url(self) -> str:
        return self._db.get(container_names.environment).get("empower_licensing_url")

    @empower_licensing_url.setter
    def empower_licensing_url(self, value: str) -> None:
        self._set(container_names.environment, "empower_licensing_url", value)

    def _set(self, container_name: str, key: str, value: any):
        self._db.dadd(container_name, (key, value))
        self._db.dump()
        print(f"{key} has been set")

    # only initialize a dictionary in the store if it doesn't exist,
    # otherwise it will clear them out
    def _initialize_dict(self, name: str):
        if not self._db.get(name):
            self._db.dcreate(name)


store = Store()

# potential future:
# @property
# def ssl(self) -> str:
#     return self._db.get('ssl')
#
# @ssl.setter
# def ssl(self, value: bool) -> None:
#     self._db.set('discovery_api_domain', value)
#     self._db.dump()
