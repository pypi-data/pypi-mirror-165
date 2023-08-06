from requests import Session

from ..urlpath import URLPath

session = Session()

BASE_URL = URLPath("https://www.vlive.tv")

DEFAULT_PARAMS = {"dataType": "json"}
