from pydogceo.PyDogCeo import PyDogCeo

class TestImages:
    def test_random(self):
        dog = PyDogCeo()
        r = dog.breed.images.random("australian")
        assert r.status_code == 200

    def test_randomNumber(self):
        dog = PyDogCeo()
        r = dog.breed.images.randomNumber("australian", 10)
        assert r.status_code == 200

    def test_subbread(self):
        dog = PyDogCeo()
        r = dog.breed.images.subbread("australian", "shepherd")
        assert r.status_code == 200
    
    def test_subbreadRandom(self):
        dog = PyDogCeo()
        r = dog.breed.images.subbreadRandom("australian", "shepherd")
        assert r.status_code == 200
    
    def test_subbreadRandomNumber(self):
        dog = PyDogCeo()
        r = dog.breed.images.subbreadRandomNumber("australian", "shepherd", 2)
        assert r.status_code == 200