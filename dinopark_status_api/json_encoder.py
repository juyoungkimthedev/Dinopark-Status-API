"""
Custom JSON Encoder

"""

# System imports
import json, bson


class MongoJsonEncoder(json.JSONEncoder):
    """
    Custom JSON encoder class
    """
    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return str(obj)

        return json.JSONEncoder.default(self, obj)
