"""
    Controller for <Mongo & SQL>
"""

from .manager import SQL, Mongo
from .manager.utils import Decode, Objects
from .types import Admin, Model, Database

Text = Model.text
JSON = Model.json
ID = Model.id


class FakeModel:
    """Fake Model for Testing"""

    def __init__(self, model):
        self.objects = model
