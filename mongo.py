from pymongo import MongoClient
from strenum import StrEnum

DATABASE_STOCKPIT = "stockpit"
COLLECTION_NASDAQ = "nasdaq"
COLLECTION_NYSE = "nyse"


class MongoOperator(StrEnum):
    LT = "$lt"
    EXISTS = "$exists"
    SET = "$set"


class Mongo:
    
    def __init__(self, user, password, authSource):
        self.user = user
        self.password = password
        self.authSource = authSource
        self.handle = None
        self.raisedError = False

    def connect(self):
        if self.handle is None:
            try:
                self.handle = MongoClient(
                    username=self.user,
                    password=self.password,
                    authSource=self.authSource
                )
                self.raisedError = False
            except:
                self.handle = None
                self.raisedError = True

    def disconnect(self):
        print(function_id())
        if self.handle:
            self.handle.close()
        self.handle = None