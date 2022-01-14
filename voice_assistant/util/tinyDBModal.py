from tinydb import TinyDB, Query


class LocalStorage(object):

    def __init__(self):
        self._database = TinyDB("../data/data.json")

    def findData(self, tableName, fieldName, value):
        """
            This function return data matching the parameters value
        :param tableName: Table on which the request is make
        :param fieldName: Field for matching
        :param value: Field value
        :return: List or dictionary matching the request
        """
        my_query = self._database.table(tableName).search(Query()[fieldName] == value)
        if type(my_query) is list and len(my_query) == 1:
            return my_query[0]
        return my_query

    def getFieldValue(self, tableName, fieldName):
        """
            This function return a table value
        :param tableName: Table on which the request is make
        :param fieldName: Field for matching
        :return: Field value if it exist
        """
        my_query = self._database.table(tableName).get(Query()[fieldName].exists())
        # if type(my_query) is list and len(my_query) == 1:
        return my_query.get(fieldName)
        # return my_query

    def getPatterns(self):
        """
            Load and return regex patterns
        :return:  Regex patterns
        """
        appLanguage = self.getFieldValue("appData", "language")
        appUtility = self.findData("appUtilities", "language", appLanguage)

        patterns = appUtility.get("patterns")

        return patterns

    def insertUsername(self, username):
        """
            This function set the user name
        :param username: The username input
        :return:
        """
        self._database.table("userData").upsert({"username": username}, Query()["username"] == "")

    def getUsername(self):
        """
            This function get the user name
        :return: The user name
        """
        my_query = self._database.table("userData").get(Query()["username"].exists())

        return my_query.get("username")
