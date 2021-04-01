

class User:
    def __init__(self, username, id):
        self.username = username
        self.id = id
        self.rooms = []
        self.messages = []
        self.directory = []

    def getName(self):
        return self.username

    def __str__(self):
        return self.username + " "+str(self.id)

    def getId(self):
        return self.id

    def setMessages(self, messages):
        self.messages = messages

    def setRooms(self, rooms):
        self.rooms = rooms

    def getMessages(self):
        return self.messages

    def getRooms(self):
        return self.rooms

    def getDirectory(self):
        return self.directory

    def setDirectory(self, dir):
        self.directory = dir
