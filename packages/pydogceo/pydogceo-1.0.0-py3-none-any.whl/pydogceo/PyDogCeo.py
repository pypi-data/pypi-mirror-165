from .routes.Breed import Breed
from .routes.Breeds import Breeds

class PyDogCeo:
    def __init__(self) -> None:
        self._breed = Breed()
        self._breeds = Breeds()

    @property
    def breed(self) -> Breed:
        return self._breed

    @property
    def breeds(self) -> Breeds:
        return self._breeds