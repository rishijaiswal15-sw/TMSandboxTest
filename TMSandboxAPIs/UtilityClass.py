class UtilityClass:

    def checkIfKeyExists(self, listOfDicts, key, value):
        if not any(keyName[key] == value for keyName in listOfDicts):
            return False
        else:
            return True
