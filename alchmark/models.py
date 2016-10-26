from bson import ObjectId
import pymongo

from alchmark.errors import APIError

connection = None


def get_connection():
    global connection
    if connection is None:
        connection = pymongo.MongoClient(host="127.0.0.1",
                                         port=27017)['alchemy']
    return connection


class Model(object):
    collection = "test"
    fields = []

    def __init__(self, **kwargs):
        self.id = kwargs.get("_id", kwargs.get("id", None))
        for field in self.fields:
            self.__dict__[field] = kwargs.get(field, None)
        self.validate()

    @staticmethod
    def get(id=None):

        return __class__(id=id)

    def create(self):
        document = self.as_dict(bson=True)
        collection = get_connection()[self.collection]
        if document["_id"]:
            document = collection.find_one({"_id": ObjectId(document['_id'])})
            if document is not None:
                raise APIError("Resource already exists.", 409)
            else:
                raise APIError("Resource not found")
        else:
            del document['_id']
        new_code = collection.insert(document)
        self.id = str(new_code)
        return self

    def as_dict(self, bson=False):
        rv = {}
        if bson:
            rv["_id"] = self.id
        else:
            rv["id"] = self.id
        for field in self.fields:
            rv[field] = self.__dict__[field]
        return rv

    def validate(self):
        pass


class User(Model):
    collection = "user"
    fields = ["name"]


class Prototype(object):
    def __init__(self):
        self.id = None
        self.name = None


class Collectible(object):
    def __init__(self):
        self.id = None
        self.prototype = None
        self.owner = None


class Recipe(object):
    def __init__(self):
        self.id = None
        self.makes = None
        self.needed = []


map = {"user": User,
       "prototype": Prototype,
       "recipe": Recipe,
       "collectible": Collectible
       }
