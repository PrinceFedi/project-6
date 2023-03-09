from datetime import datetime

from mongoengine import *


class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
        km: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open: MongoEngine string field, required, (checkpoint opening time),
		close MongoEngine string field, required, (checkpoint closing time).
    """
    km = FloatField(required=True)
    miles = FloatField(required=True)
    location = StringField(required=False)
    open = StringField(required=True)
    close = StringField(required=True)

class Brevet(Document):
    """
    A MongoEngine document containing:
		length: MongoEngine float field, required
		start_time: MongoEngine string field, required
		checkpoints: MongoEngine list field of Checkpoints, required
    """
    length = FloatField(required=True)
    start_time = StringField(required=True)
    checkpoints = EmbeddedDocumentListField(Checkpoint, required=True)

