class Context:

    _all_services:dict[str, any] = {}

    def __init__(self, serviceConfiguration: dict[str, any]):
        self._all_services = serviceConfiguration

    def get_service(self, key: str) -> any:
        if key not in self._all_services:
            raise Exception(f"Service with key {key} not registered!")

        return self._all_services.get(key)
    
    def run_on_service(self, key: str, delegate) -> None:
        if key not in self._all_services:
            return
        
        delegate(self._all_services[key])
