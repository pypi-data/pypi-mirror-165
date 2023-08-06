
PyDogCeo
===========


PyDogCeo is a thin wrapper on top of the [DogCEO-API](https://dog.ceo). 
[DOG-CEO on GITHUB](https://github.com/ElliottLandsborough/dog-ceo-api)


To Start...
-----------

To install pydogceo:

```bash
pip install pydogceo
```


Using it...
-----------

All methods return a requests Response Object representing the raw response from the API. Any HTTP errors that are returned by the API are
raised as HTTPError exceptions from the Requests library.

```python
from pydogceo import PyDogCeo

dog = PyDogCeo()
r = dog.breeds.listAll()
```


Available Methods/ Endpoints
----------
```python
dog.breeds.listAll()
dog.breeds.listAllRandom()
dog.breeds.listAllRandomNumber(10)
dog.breeds.listMaster()
dog.breeds.listMasterRandom()
dog.breeds.listMasterRandomNumber(3)

dog.breeds.image.random()
dog.breeds.image.randomNumber(3)

dog.breed.subbreed("hound")
dog.breed.subbreedRandom("hound")
dog.breed.subbreedRandomNumber("hound", 3)

dog.breed.image("hound")

dog.breed.images.random("hound")
dog.breed.images.randomNumber("hound", 4)

dog.breed.images.subbread("hound", "afghan")
dog.breed.images.subbreadRandom("hound", "afghan")
dog.breed.images.subbreadRandomNumber("hound", "afghan", 10)
```


Changelog
---------

v0.0.1- 28/08/2022

~~~~~~~~~~~~~~~~~

First Release :)
