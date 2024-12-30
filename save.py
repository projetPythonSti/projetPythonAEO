import json

from collections import defaultdict

class JSONSerializable:
    """Mixin class to enable JSON serialization of objects."""
    def to_dict(self):
        """Convert object attributes to a dictionary."""
        print(f"je to_dict {self}")
        result = {}
        for attr, value in self.__dict__.items():
            if isinstance(value, (list, dict, tuple, set)):
                result[attr] = self._serialize_collection(value)
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            else:
                result[attr] = value
        return result

    @staticmethod
    def _serialize_collection(collection):
        """Serialize lists, dictionaries, sets, or tuples."""
        print(f"je _serialize_collection {collection}")
        if isinstance(collection, list):
            return [item.to_dict() if hasattr(item, "to_dict") else item for item in collection]
        elif isinstance(collection, (dict, defaultdict)):
            return {
                key: value.to_dict() if hasattr(value, "to_dict") else value
                for key, value in collection.items()
            }
        elif isinstance(collection, (tuple, set)):
            return [item.to_dict() if hasattr(item, "to_dict") else item for item in collection]
        return collection

    def to_json(self, file_path=None):
        """Convert object to JSON and optionally save to file."""
        data = self.to_dict()
        if file_path:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
        return json.dumps(data, indent=4)