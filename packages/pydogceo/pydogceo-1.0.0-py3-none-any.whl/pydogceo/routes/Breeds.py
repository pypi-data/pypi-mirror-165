from ..request.BaseRequest import BaseRequests
from .Image import Image
from requests import Response

class Breeds(BaseRequests):
    def __init__(self) -> None:
        self._image = Image()
        super().__init__()

    def listAll(self) -> Response:
        """ List all breed names including sub breeds.

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET("/breeds/list/all")
    
    def listAllRandom(self) -> Response:
        """ Get random breed including any sub breeds.

        Returns:
            :class:`Response <Response>` object
        """        
        return self.GET("/breeds/list/all/random")
    
    def listAllRandomNumber(self, number: int) -> Response:
        """Get {number} random breeds including any sub breeds.

        Args:
            number (int): Number of random breeds

        Returns:
                :class:`Response <Response>` object
        """        
        return self.GET(f"/breeds/list/random/{number}")
    
    def listMaster(self) -> Response:
        """ List all master breed names.

        Returns:
            :class:`Response <Response>` object
        """        

        return self.GET("/breeds/list")

    def listMasterRandom(self) -> Response:
        """ Get single random master breed.

        Returns:
            :class:`Response <Response>` object
        """        

        return self.GET("/breeds/list")
    
    def listMasterRandomNumber(self, number: int) -> Response:
        """Get {number} random master breeds.

        Args:
            number (int): Number of random master breeds

        Returns:
                :class:`Response <Response>` object
        """        
        return self.GET(f"/breeds/list/random/{number}")
    
    @property
    def image(self) -> Image:
        return self._image