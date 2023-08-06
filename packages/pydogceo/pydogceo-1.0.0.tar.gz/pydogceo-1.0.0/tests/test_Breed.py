from pydogceo.PyDogCeo import PyDogCeo

class TestBreed:
    def test_subbreed(self):
        dog = PyDogCeo()
        r = dog.breed.subbreed("terrier")
        assert r.status_code == 200

    def test_subbreedRandom(self):
        dog = PyDogCeo()
        r = dog.breed.subbreedRandom("terrier")
        assert r.status_code == 200

    def test_subbreedRandomNumber(self):
        dog = PyDogCeo()
        r = dog.breed.subbreedRandomNumber("terrier", 2)
        assert r.status_code == 200
    
    def test_images(self):
        dog = PyDogCeo()
        r = dog.breed.image("terrier")
        assert r.status_code == 200
