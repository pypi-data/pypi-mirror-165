from requests import Session, Response
from ..config.BaseConfiguration import BaseConfiguration

class BaseRequests(BaseConfiguration):
    def __init__(self) -> None:
        self.session = Session()

    def GET(self, requestUrl: str) -> Response:
        return self.session.get(self.createRequestUrl(requestUrl), timeout=self.BASE_REQUEST_TIMEOUT)
    
    def createRequestUrl(self, requestUrl) -> str:
        return self.BASE_API_URL + requestUrl

