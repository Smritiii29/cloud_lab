
class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def __str__(self):
        return f"DataObject(name={self.name}, values={self.values})"
