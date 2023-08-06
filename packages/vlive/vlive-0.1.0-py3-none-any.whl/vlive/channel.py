from .models import ChannelProfile
from .session import BASE_URL, session


class Channel:
    @staticmethod
    def profile(code: str):
        res = session.get(
            BASE_URL / "globalv-web/vam-web/vhs/store/v1.0/channels" / code,
            params={"platformType": "PC"},
            headers={
                "Referer": f"https://www.vlive.tv/channel/{code}",
            },
        )
        if not res.ok:
            raise ConnectionError(f"{res.status_code}: {res.text}")
        data = res.json()
        return ChannelProfile(**data)


channel = Channel()
