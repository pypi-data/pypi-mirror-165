class URLPath:
    def __init__(self, base_url: str, path: str = ""):
        self.base_url = base_url.rstrip("/")
        self.path = f"/{path.lstrip('/')}"
        self.url = f"{self.base_url}/{self.path.lstrip('/')}"

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.__str__()

    def __truediv__(self, other: str):
        path = f'{self.path.strip("/")}/{other.lstrip("/")}'
        return URLPath(self.base_url, path)
