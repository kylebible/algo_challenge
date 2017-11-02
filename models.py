from mongoengine import *
import os

DEVELOP = int(os.environ['DEVELOP'])

if DEVELOP:
    mongo_url = "mongodb://localhost:27017"
    db = 'testdb2'
else:
    mongo_url = os.environ["MONGODB_URI"]
    db = 'algo'

connect(db=db,
        host=mongo_url,
        connectTimeoutMS=30000,
        socketTimeoutMS=None,
        socketKeepAlive=True)


class User(Document):
    id = StringField(primary_key=True)
    username = StringField()
    last_lead = DateTimeField()

class Team(EmbeddedDocument):
    members = ListField(ReferenceField(User))

class Challenge(Document):
    title = StringField()
    description = StringField()
    difficulty = StringField()
    votes = ListField(ReferenceField(User))


class Game(Document):
    teams = ListField(EmbeddedDocumentField(Team))
    challenge = ReferenceField(Challenge)
    choices = ListField(ReferenceField(Challenge))
    solution = StringField()



