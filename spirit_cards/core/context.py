class Context:

    _all_services: dict[str, any]

    def __init__(self, serviceConfiguration: dict[str, any]):
        self._all_services = serviceConfiguration

    def set_service(self, key: str, service: any) -> any:
        self._all_services[key] = service

    def get_service(self, key: str) -> any:
        if key not in self._all_services:
            raise Exception(f"Service with key {key} not registered!")

        return self._all_services.get(key)

class ScopedContext(Context):

    _scoped_services: dict[str, any]

    base_context: Context

    def __init__(self, base_context: Context, serviceConfiguration: dict[str, any]):
        self.base_context = base_context
        self._scoped_services = serviceConfiguration

    def set_service(self, key: str, service: any) -> any:
        self._scoped_services[key] = service

    def get_service(self, key: str) -> any:
        if key not in self._scoped_services:
            return self.base_context.get_service(key)

        return self._scoped_services.get(key)
    
    def cleanup(self):
        self._scoped_services.clear()
    