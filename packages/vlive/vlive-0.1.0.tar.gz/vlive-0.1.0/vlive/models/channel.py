from pydantic import AnyHttpUrl, BaseModel


class Channel(BaseModel):
    name: str
    icon: AnyHttpUrl
    type: str
    code: str

    def __str__(self):
        return self.name
