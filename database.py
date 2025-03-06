
import pandas as pd
#create a class for representing a database. The database is going to be a set of key value pairs stored in a pandas dataframe

class DataBase():
    def __init__(self):
        self._data = pd.DataFrame()

    def get(self, key):
        return self._data[key]

    def put(self, key, value):
        self._data[key] = value
        return self._data[key].fillna("")

    def all(self):
        return self._data.fillna("")
    
    def delete(self, key):
        self._data.pop(key)
        return self._data.fillna("")

    def clear_all(self):
        self._data = pd.DataFrame()
        return self._data