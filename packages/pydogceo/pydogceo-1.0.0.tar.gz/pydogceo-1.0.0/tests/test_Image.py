from pydogceo.PyDogCeo import PyDogCeo

class TestImage:
    def test_random(self):
        dog = PyDogCeo()
        r = dog.breeds.image.random()
        assert r.status_code == 200

    def test_random_number(self):
        dog = PyDogCeo()
        r = dog.breeds.image.randomNumber(2)
        assert r.status_code == 200