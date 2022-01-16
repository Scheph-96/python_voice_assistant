import os
from pathlib import Path

from tinydb import TinyDB, Query
from tinydb.operations import add


class LocalStorage(object):
    """
        This is a class for managing data input and output

        :attributes: None
    """

    def __init__(self):
        """
            The constructor for localStorage Class
        """
        self.__database = TinyDB(os.fspath(Path(__file__).resolve().parent.parent / "data/data.json"), sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

    def findData(self, tableName, fieldName, value):
        """
            This function return data matching the parameters value
        :param tableName: string: Table on which the request is make
        :param fieldName: string: Field for matching
        :param value: string: Field value
        :return: List or Dictionary: Results matching the result
        """
        my_query = self.__database.table(tableName).search(Query()[fieldName] == value)
        if type(my_query) is list and len(my_query) == 1:
            return my_query[0]
        return my_query

    def getFieldValue(self, tableName, fieldName):
        """
            This function return some table field value
        :param tableName: string: Table on which the request is make
        :param fieldName: string: Field for matching
        :return: string: Field value if it exist
        """
        my_query = self.__database.table(tableName).get(Query()[fieldName].exists())
        # if type(my_query) is list and len(my_query) == 1:
        return my_query.get(fieldName)
        # return my_query

    def getPatterns(self):
        """
            This function load and return regex patterns
        :return: Dictionary: Regex patterns
        """
        appLanguage = self.getFieldValue("appData", "language")
        appUtility = self.findData("appUtilities", "language", appLanguage)

        patterns = appUtility.get("patterns")

        return patterns

    def insertUsername(self, username):
        """
            This function set the user name
        :param username: string: The username input
        :return:
        """
        self.__database.table("userData").upsert({"username": username}, Query()["username"] == "")

    def getUsername(self):
        """
            This function get the user name
        :return: string: The user name
        """
        my_query = self.__database.table("userData").get(Query()["username"].exists())

        return my_query.get("username")

    def insertMemorize(self, memory):
        """
            This function inserts new information to remember
        :param memory: dictionary: Memories pattern
        :return:
        """
        self.__database.table("userData").update(add("memorize", [memory]), Query()["memorize"].exists())
