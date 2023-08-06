from pydogceo.PyDogCeo import PyDogCeo
from pprint import pprint


dog = PyDogCeo()

r = dog.breeds.listAll()
r = dog.breeds.listAllRandom()
r = dog.breeds.listAllRandomNumber(10)
r = dog.breeds.listMaster()
r = dog.breeds.listMasterRandom()
r = dog.breeds.listMasterRandomNumber(3)

r = dog.breeds.image.random()
r = dog.breeds.image.randomNumber(3)

r = dog.breed.subbreed("hound")
r = dog.breed.subbreedRandom("hound")
r = dog.breed.subbreedRandomNumber("hound", 3)

r = dog.breed.image("hound")

r = dog.breed.images.random("hound")
r = dog.breed.images.randomNumber("hound", 4)

r = dog.breed.images.subbread("hound", "afghan")
r = dog.breed.images.subbreadRandom("hound", "afghan")
r = dog.breed.images.subbreadRandomNumber("hound", "afghan", 10)


json = r.json()

pprint(json["message"])