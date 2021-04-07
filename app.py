from utils.utils import errorMessage, successMessage, customMessage, displayFeatures
from services.firebaseservice import FirebaseService
import time

from dotenv import load_dotenv
import os


def main():
    successMessage("Starting FireChat")
    service = FirebaseService(os.getenv("PROJECT_URL"))

    displayFeatures()

    while True:

        if service.currentUser != None:
            customMessage("     Logged in as " + service.currentUser.getName() +
                          " " + str(service.currentUser.getId()))
        else:
            print()
            customMessage("     You are not logged in.      ")
            print()
        try:
            print("""1: Signup\n2: Signin\n3: Get Current User \n4: Send message\n5: See messages from user\n6: Lookup directory\n7: See online users\n8: Stream chat\n9: Create Group\n10: Add user to group\n11: Send message to group\n12: Listen to group stream\n""")
            choice = int(
                input(":>"))

            # choice = 8
            if choice == 1:
                username = input("Username :> ")
                empId = int(input("ID :> "))
                password = input("Password :> ")
                service.signUpUser(username, empId, password)
            elif choice == 2:
                username = input("Username :> ")
                password = input("Password :> ")
                service.signInUser(username, password)

            elif choice == 3:
                print("")
                print(service.getCurrentUser())
                print("")
            elif choice == 4:
                service.updatesMessagesForUsers()
                receiverId = int(input("Receiver id :> "))
                while True:
                    msg = input("{}:> ".format(
                        service.getNameFromDirectory(Id=service.getCurrentUserId())))
                    if msg == "q":
                        break
                    service.sendMessage(receiverId, msg)

            elif choice == 5:
                senderId = int(input("Sender id :> "))

                service.seeMessages(senderId)
            elif choice == 6:
                service.lookupDirectory()
            elif choice == 7:
                service.getOnlineUsers()
            elif choice == 8:
                # warningMessage("Stream available only for two minutes.")
                senderId = int(input("Sender id :> "))
                service.seeLiveMessage(senderId)
                time.sleep(1200)
                service.closeStream()

            elif choice == 9:
                service.updateDirectory()

                groupId = service.createGroup()

                service.lookupDirectory()
                while True:
                    try:
                        userId = int(
                            input("Enter user id to add to group :> "))
                        service.addUserToGroup(groupId, userId)
                    except ValueError:
                        break

            elif choice == 10:
                service.updateDirectory()

                service.getOwnedGroups()

                userid = int(input("Enter user id :> "))
                groupId = input("Enter group id :> ")
                service.addUserToGroup(groupId, userid)

            elif choice == 11:
                # Send message to group

                service.updateDirectory()

                _ = service.getGroups()
                groupId = input("Enter group id :> ")

                while True:
                    msg = input("{}:> ".format(
                        service.getNameFromDirectory(Id=service.getCurrentUserId())))
                    service.sendMessageToGroup(msg, groupId)

                    if msg == "q":
                        break
            elif choice == 12:
                # warningMessage("Stream available only for two minutes.")
                service.updateDirectory()

                _ = service.getGroups()

                groupId = input("Group id :> ")
                service.seeLiveMessagesFromGroup(groupId)

                time.sleep(1200)
                service.closeStream()
            else:
                service.goOffline()
                service.closeStream()
                exit()
        except Exception as e:
            errorMessage(e)
            service.goOffline()
            exit()


load_dotenv(".env", verbose=True)
main()
