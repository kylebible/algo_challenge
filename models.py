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
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(User, self).save(*args, **kwargs)

class Team(EmbeddedDocument):
    members = ListField(ReferenceField(User))
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(Team, self).save(*args, **kwargs)

class Challenge(Document):
    title = StringField()
    description = StringField()
    difficulty = StringField()
    url = URLField()
    votes = ListField(ReferenceField(User))
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(Challenge, self).save(*args, **kwargs)


class Game(Document):
    teams = ListField(EmbeddedDocumentField(Team))
    challenge = ReferenceField(Challenge)
    choices = ListField(ReferenceField(Challenge))
    solution = StringField()
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(Game, self).save(*args, **kwargs)



