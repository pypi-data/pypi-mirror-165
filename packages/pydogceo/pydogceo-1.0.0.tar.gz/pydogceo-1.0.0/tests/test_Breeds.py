from pydogceo.PyDogCeo import PyDogCeo

class TestBreeds:
    def test_listAll(self):
        dog = PyDogCeo()
        r = dog.breeds.listAll()
        assert r.status_code == 200

    def test_listAllRandom(self):
        dog = PyDogCeo()
        r = dog.breeds.listAllRandom()
        assert r.status_code == 200

    def test_listAllRandomNumber(self):
        dog = PyDogCeo()
        r = dog.breeds.listAllRandomNumber(2)
        assert r.status_code == 200
    
    def test_listMaster(self):
        dog = PyDogCeo()
        r = dog.breeds.listMaster()
        assert r.status_code == 200
    
    def test_listMasterRandom(self):
        dog = PyDogCeo()
        r = dog.breeds.listMasterRandom()
        assert r.status_code == 200
    
    def test_listMasterRandomNumber(self):
        dog = PyDogCeo()
        r = dog.breeds.listMasterRandomNumber(5)
        assert r.status_code == 200