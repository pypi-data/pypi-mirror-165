from ..request.BaseRequest import BaseRequests
from .Images import Images
from requests import Response

class Breed(BaseRequests):
    def __init__(self) -> None:
        self._images = Images()
        super().__init__()

    def subbreed(self, breed: str) -> Response:
        """ List sub breeds.

        Args:
            breed (str): Breed

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/list")

    def subbreedRandom(self, breed: str) -> Response:
        """ List {number} of sub breeds of breed.

        Args:
            breed (str): Breed

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/list/random")

    def subbreedRandomNumber(self, breed: str, number: int) -> Response:
        """ List {number} of sub breeds of breed.

        Args:
            breed (str): Breed
            number (int): Number of random subbreeds

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/list/random/{number}")
    
    def image(self, breed: str) -> Response:
        """ Get all breed images.

        Args:
            breed (str): Breed

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET(f"/breed/{breed}/images")


    @property
    def images(self) -> Images:
        return self._images
