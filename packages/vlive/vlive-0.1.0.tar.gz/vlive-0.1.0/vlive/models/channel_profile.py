from pydantic import AnyHttpUrl, BaseModel, conint


class ChannelProfile(BaseModel):
    profileImg: AnyHttpUrl
    name: str
    latestUpdatedAt: conint(ge=0)
    channelCode: str
