from .models import Channel
from .session import BASE_URL, DEFAULT_PARAMS, session


class Search:
    @staticmethod
    def channels(query: str, max_rows: int = 10):
        res = session.get(
            BASE_URL / "search" / "auto" / "channels",
            params={
                **DEFAULT_PARAMS,
                "query": query,
                "maxNumOfRows": max_rows,
            },
        )
        if not res.ok:
            raise ConnectionError(f"{res.status_code}: {res.text}")
        data = res.json()
        channels = [Channel(**d) for d in data]
        return channels


search = Search()
