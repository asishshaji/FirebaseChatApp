from prettytable import PrettyTable
import pyrebase
from utils.utils import hashPassword
from utils.utils import successMessage, warningMessage, errorMessage, leftPrint, rightPrint, customMessage
from models.user import User
import time
import types
import timeago
import datetime
import random
import string
import secrets


class FirebaseService:

    def __init__(self, authDomain):
        self.authDomain = "{}.firebaseapp.com".format(authDomain)
        self.databaseURL = "https://{}.firebaseio.com".format(authDomain)
        self.storageBucket = "{}.appspot.com".format(authDomain)
        self.firebaseDB = pyrebase.initialize_app({
            "authDomain": self.authDomain,
            "databaseURL": self.databaseURL,
            "storageBucket": self.storageBucket,
            "apiKey": "apikey"
        }).database()

        self.currentUser = None

        self.stream = None

    def getCurrentUser(self):
        """Get the current user

        Returns:
            User: current user
        """
        return self.currentUser

    def getCurrentUserId(self):
        """Get logged in user's employee id

        Returns:
            int: employee id
        """
        return self.currentUser.getId()

    def signUpUser(self, username, id, password):
        """Sign up the user with given credentials
           Given password is changed to its sha equivalent

        Args:
            username (str): username of the user
            id (int): employee id
            password (str): password of the user in plain text
        """
        encodedPassword = hashPassword(password)
        if not self.checkUserExistsByUsername(username):
            self.firebaseDB.child("users").child(id).set({
                "username": username,
                "id": id,
                "password": encodedPassword,

            })
            self.firebaseDB.child("onlineStatus").child(id).set({
                "online": False,
            })

            successMessage("User created successfully")
        else:
            warningMessage("{} already exists".format(username))

    def signInUser(self, username, password):
        """Sign in for user

        Args:
            username (str): username of user
            password (str): password of user
        """
        successMessage("Connecting to authentication service")
        encodedPassword = hashPassword(password)
        actualPassword = self.getUser(username)[0].val()['password']
        if actualPassword == encodedPassword:
            successMessage("Authenticated.")
            user = self.getUser(username)[0].val()
            self.currentUser = User(username=user['username'], id=user['id'])
            self.firebaseDB.child("onlineStatus").child(user['id']).set({
                "online": True,
            })
        else:
            errorMessage("Invalid credentials.")

    def goOffline(self):
        """User online status is set to false
        """
        userId = self.currentUser.getId()

        self.firebaseDB.child("onlineStatus").child(userId).set({
            "online": False,
        })

    def getUser(self, username):
        """Gets user using username

        Args:
            username (str): username of user

        Returns:
            User: User having username as username
        """
        users = self.firebaseDB.child("users").order_by_child(
            "username").equal_to(username).get()
        if len(users.each()) != 0:
            return users.each()

    def checkUserExistsByUsername(self, username):
        """Checks if user with username exists

        Args:
            username (str): username to check

        Returns:
            bool: True if user exists, False if doesnot exists
        """
        users = self.firebaseDB.child("users").order_by_child(
            "username").equal_to(username).get()
        if len(users.each()) == 0:
            return False
        return True

    def checkUserExistsById(self, id):
        """Check if user with employeeId id exists

        Args:
            id (int): employee id of user

        Returns:
            bool: True if exists else False
        """
        users = self.firebaseDB.child("users").child(id).get()
        if len(users.each()) == 0:
            return False
        return True

    def sendMessage(self, receiverId, msg):
        """Send message to receiver having the id as receiverId

        Args:
            receiverId (int): employee id of receiver
            msg (str): message to send
        """
        if self.checkUserExistsById(receiverId):
            successMessage("Message sent to {}" .format(
                self.getNameFromDirectory(receiverId)))

            currentUserId = self.currentUser.getId()

            # create room for users
            roomId = receiverId + currentUserId
            timestamp = str(time.time()).split(".")[0]
            now = time.strftime("%Y-%m-%d %H:%M:%S")

            self.firebaseDB.child("messages").child(roomId).child(timestamp).set({
                "message": msg,
                "sender": currentUserId,
                "receiver": receiverId,
                "timestamp": now,
            })

        else:
            errorMessage("User does not exists")

    def updateDirectory(self):
        """Updates the local User object
        """
        users = self.firebaseDB.child("users").get()
        directory = []
        if users.val() != None:
            for user in users.each():
                directory.append({
                    "username": user.val()['username'],
                    "id": user.val()['id']
                })

        self.currentUser.setDirectory(directory)

    def updatesMessagesForUsers(self):
        """Updates messages for local User
        """
        self.updateDirectory()

        currentUserId = self.currentUser.getId()

        messages = self.firebaseDB.child("messages").get()
        if(messages.val() != None):
            roomId = []
            msgs = []
            for message in messages.each():
                if self.checkUserExistsById(int(message.key()) - currentUserId):
                    roomId.append(int(message.key()))
                    msgs.append(message.val())

            self.currentUser.setMessages(msgs)
            self.currentUser.setRooms(roomId)

    def getMessagesFromRoom(self, roomId, sender, receiver):
        """Get messages for user

        Args:
            roomId (int): 
            sender (int): 
            receiver (int): 
        """
        print("Chat dump")
        print("---------------------------------------------------------------")

        messages = self.currentUser.getMessages()

        for msg in messages:
            for stamp, data in msg.items():
                if data['receiver'] == receiver:
                    leftPrint(data['message'])
                    leftPrint("-"*30)
                    leftPrint(timeago.format(
                        data["timestamp"], time.strftime(
                            "%Y-%m-%d %H:%M:%S")
                    ))
                    leftPrint("")
                else:
                    rightPrint(data['message'])
                    rightPrint("-"*30)
                    rightPrint(timeago.format(
                        data["timestamp"], time.strftime(
                            "%Y-%m-%d %H:%M:%S")
                    ))
                    rightPrint("")

    def lookupDirectory(self):
        """Username and employee id is printed
        """
        self.updatesMessagesForUsers()
        t = PrettyTable(['Name', 'ID'])
        dir = self.currentUser.getDirectory()

        names = [d['username'] for d in dir]
        ids = [d['id'] for d in dir]

        for i in range(len(names)):
            t.add_row([names[i], ids[i]])

        print(t)

    def getOnlineUsers(self):
        """Prints the list of online users
        """
        self.updatesMessagesForUsers()

        t = PrettyTable(['Name', 'ID'])
        t.title = "Online users"

        online = self.firebaseDB.child("onlineStatus").get()

        userIDS = [int(o.key())
                   for o in online.each() if o.val()['online'] == True]

        directory = self.currentUser.getDirectory()

        for id in userIDS:
            user = list(filter(lambda u: u['id'] == id, directory))
            t.add_row([user[0]['username'], id])

        print(t)

    def getNameFromDirectory(self, Id):
        """Get the name of the user from employee id

        Args:
            Id (int): employee id

        Returns:
            str: username of the employee
        """
        directory = self.currentUser.getDirectory()
        for d in directory:
            if d['id'] == Id:
                return d['username']

    def stream_handler(self, message):
        """Stream handler for messages

        Args:
            message (str): stream object
        """

        receiver = self.currentUser.getId()

        if len(message["data"]) == 4:
            now = time.strftime("%Y-%m-%d %H:%M:%S")

            print()
            customMessage("New message from {}".format(
                self.getNameFromDirectory(message["data"]["sender"])))
            print("[{0}] :> {1}".format(self.getNameFromDirectory(
                message["data"]["sender"]), message["data"]["message"]), "({})".format(timeago.format(message["data"]["timestamp"], now)))
            print()
        else:
            for val in message["data"]:
                now = time.strftime("%Y-%m-%d %H:%M:%S")

                print()
                print("[{0}] :> {1}".format(self.getNameFromDirectory(
                    message["data"][val]["sender"]), message["data"][val]["message"]), "({})".format(timeago.format(message["data"][val]["timestamp"], now)))
                print()

    def closeStream(self):
        """Close the stream
        """
        self.stream.close()

    def seeLiveMessage(self, senderId):
        """Print live messages from stream

        Args:
            senderId (int): employee id of the sender
        """

        self.updatesMessagesForUsers()

        userRooms = self.currentUser.getRooms()
        currentUserId = self.currentUser.getId()

        online = self.firebaseDB.child("onlineStatus").get()

        directory = self.currentUser.getDirectory()

        roomIds = []
        for room in userRooms:
            if room == currentUserId + senderId:
                roomIds.append(room)

        try:
            self.stream = self.firebaseDB.child("messages").child(
                roomIds[0]).stream(stream_handler=self.stream_handler)

        except Exception as e:
            print(e)

    def seeMessages(self, senderId):
        """See all the messages from sender

        Args:
            senderId (int): employee of the sender
        """
        self.updatesMessagesForUsers()
        userRooms = self.currentUser.getRooms()
        currentUserId = self.currentUser.getId()

        roomIds = []
        for room in userRooms:
            if room == currentUserId + senderId:
                roomIds.append(room)

        for room in roomIds:
            self.getMessagesFromRoom(room, senderId, currentUserId)

    def createGroup(self):
        """Creates group with random id

        Returns:
           str: returns id of created group
        """
        res = ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                      for i in range(30))

        self.firebaseDB.child("groups").child(res).update(
            {"admin": self.currentUser.getId()})

        self.firebaseDB.child("messages").child(res)

        return res

    def addUserToGroup(self, groupId, userid):
        """Adds user to group with group id

        Args:
            groupId (int): Group id
            userid (int): Employee id
        """
        group = self.firebaseDB.child("groups").child(groupId).get()

        admin = group.val()['admin']
        print("admin is")
        if self.currentUser.getId() == admin:
            self.firebaseDB.child("groups").child(
                groupId).update({userid: userid})
            successMessage("Added {} to group".format(userid))
        else:
            errorMessage("You are not the admin")

    def getOwnedGroups(self):
        """Get current users group
        """
        currentUserId = self.currentUser.getId()

        groups = self.firebaseDB.child("groups").order_by_child(
            "admin").equal_to(currentUserId).get()

        groups = [group.key() for group in groups.each()]

        t = PrettyTable(['Group IDs'])
        t.add_rows([groups])

        print(t)

    def getGroups(self):
        """Print all the groups of user

        Returns:
            list: list of groups
        """
        currentUserId = self.currentUser.getId()

        groupsRef = self.firebaseDB.child("groups").get()

        groups = []

        for group in groupsRef.each():
            if group.val()['admin'] == currentUserId or group.val()[str(currentUserId)] == currentUserId:
                groups.append(group.key())

        t = PrettyTable(['Group IDs'])
        t.add_rows([groups])

        print(t)

        return groups

    def sendMessageToGroup(self, msg, groupId):
        """Send message to group

        Args:
            msg (str): message to send
            groupId (int): group id
        """
        currentUserId = self.currentUser.getId()
        timestamp = str(time.time()).split(".")[0]
        now = time.strftime("%Y-%m-%d %H:%M:%S")

        self.firebaseDB.child("group_messages").child(groupId).child(timestamp).set({
            "message": msg,
            "sender": currentUserId,
            "receiver": groupId,
            "timestamp": now,
        })

    def liveStreamHandler(self, message):
        # print(message["data"])

        msg = message["data"]

        if len(msg) == 4:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            leftPrint(msg["message"])
            senderName = self.getNameFromDirectory(msg["sender"])
            customMessage("New message from {}".format(senderName))
            print("[{0}] :> {1}".format(self.getNameFromDirectory(
                msg["sender"]), msg["message"]), "({})".format(timeago.format(msg["timestamp"], now)))
            print()

        else:
            for val in msg:
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                print()
                print("[{0}] :> {1}".format(self.getNameFromDirectory(
                    msg[val]["sender"]), msg[val]["message"]), "({})".format(timeago.format(msg[val]["timestamp"], now)))
                print()

    def seeLiveMessagesFromGroup(self, groupId):

        # check if current user is part of the group
        try:
            self.stream = self.firebaseDB.child("group_messages").child(
                groupId).stream(stream_handler=self.liveStreamHandler)
        except Exception as e:
            print(e)
            print("Error")
