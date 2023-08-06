from pydogceo.request.BaseRequest import BaseRequests

from ..request.BaseRequest import BaseRequests
from requests import Response

class Images(BaseRequests):
    def __init__(self) -> None:
        super().__init__()
    
    def random(self, breed: str) -> Response:
        """ Get random image from a breed (and all its sub-breeds).

        Args:
            breed (str): Name of breed

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/images/random")

    def randomNumber(self, breed: str, number: int) -> Response:
        """ Get {number} random images from a breed (and all its sub-breeds).

        Args:
            breed (str): Name of breed
            number (int): Number of random master breeds

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/images/random/{number}")

    def subbread(self, breed: str, subbreed: str) -> Response:
        """ Get all images from a sub breed.

        Args:
            breed (str): Name of breed
            subbreed (str): Name of subbreed

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/{subbreed}/images/")

    def subbreadRandom(self, breed: str, subbreed: str) -> Response:
        """ Get random image from a sub breed.

        Args:
            breed (str): Name of breed
            subbreed (str): Name of subbreed

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/{subbreed}/images/random")

    def subbreadRandomNumber(self, breed: str, subbreed: str, number: int) -> Response:
        """ Get {number} random images from a sub breed.

        Args:
            breed (str): Name of breed
            subbreed (str): Name of subbreed
            number (int): Number of random master breeds

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/{subbreed}/images/random/{number}")