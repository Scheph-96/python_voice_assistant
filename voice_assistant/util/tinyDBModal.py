from tinydb import TinyDB, Query


class LocalStorage(object):

    def __init__(self):
        self._database = TinyDB("../data/data.json")

    def findData(self, tableName, fieldName, value):
        my_query = self._database.table(tableName).search(Query()[fieldName] == value)
        if type(my_query) is list and len(my_query) == 1:
            return my_query[0]
        return my_query

    def getFieldValue(self, tableName, fieldName):
        my_query = self._database.table(tableName).get(Query()[fieldName].exists())
        # if type(my_query) is list and len(my_query) == 1:
        return my_query.get(fieldName)
        # return my_query

    def getPatterns(self):
        appLanguage = self.getFieldValue("appData", "language")
        appUtility = self.findData("appUtilities", "language", appLanguage)

        patterns = appUtility.get("patterns")

        return patterns
