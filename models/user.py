

class User:
    def __init__(self, username, id):
        """User

        Args:
            username (str): username of the employee
            id (int): employee id
        """
        self.username = username
        self.id = id
        self.rooms = []
        self.messages = []
        self.directory = []

    def getName(self):
        """Gets current users name

        Returns:
            str: username
        """
        return self.username

    def __str__(self):
        return self.username + " "+str(self.id)

    def getId(self):
        """Get current users id

        Returns:
            str: user id
        """
        return self.id

    def setMessages(self, messages):
        """Saves messages to User object

        Args:
            messages (list): messages to save
        """
        self.messages = messages

    def setRooms(self, rooms):
        """Saves rooms to User object

        Args:
            rooms (list): rooms to save
        """
        self.rooms = rooms

    def getMessages(self):
        """Get all the messages

        Returns:
            list: messages
        """
        return self.messages

    def getRooms(self):
        """Get all the rooms

        Returns:
            list: all the rooms
        """
        return self.rooms

    def getDirectory(self):
        """Get the directory

        Returns:
            list: directory
        """
        return self.directory

    def setDirectory(self, dir):
        """Saves directory

        Args:
            dir (list): directory to save
        """
        self.directory = dir
