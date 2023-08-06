from pydogceo.request.BaseRequest import BaseRequests


from ..request.BaseRequest import BaseRequests
from requests import Response

class Image(BaseRequests):
    def __init__(self) -> None:
        super().__init__()

    def random(self) -> Response:
        """ Random image from any breed.

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET("/breeds/image/random")
    
    def randomNumber(self, number: int) -> Response:
        """ Get {number} random images from any breed (max. 50)

        Args:
            number (int): Number of random breeds

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breeds/image/random/{number}")