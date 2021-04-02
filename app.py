from utils.utils import successMessage, leftPrint, rightPrint, customMessage, warningMessage, displayFeatures
from services.firebaseservice import FirebaseService


def main():
    successMessage("Starting FireChat")
    service = FirebaseService("usttest-89c43-default-rtdb")

    displayFeatures()

    while True:

        if service.currentUser != None:
            customMessage("     Logged in as " +
                          service.currentUser.getName()+"having id  "+str(service.currentUser.getId()))
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
                id = int(input("ID :> "))
                password = input("Password :> ")
                service.signUpUser(username, id, password)
            elif choice == 2:
                username = input("Username :> ")
                password = input("Password :> ")
                service.signInUser(username,  password)

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
                warningMessage("Stream available only for two minutes.")
                senderId = int(input("Sender id :> "))
                service.seeLiveMessage(senderId)
                import time
                time.sleep(120)
                service.closeStream()

            elif choice == 9:
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
                service.getOwnedGroups()

                userid = int(input("Enter user id :> "))
                groupid = input("Enter group id :> ")
                service.addUserToGroup(groupid, userid)

            elif choice == 11:
                # Send message to group

                service.updateDirectory()

                groups = service.getGroups()
                groupId = input("Enter group id :> ")

                while True:
                    msg = input("{}:> ".format(
                        service.getNameFromDirectory(Id=service.getCurrentUserId())))
                    service.sendMessageToGroup(msg, groupId)

                    if msg == "q":
                        break
            elif choice == 12:
                warningMessage("Stream available only for two minutes.")

                _ = service.getGroups()

                groupId = int(input("Group id :> "))
                service.seeLiveMessagesFromGroup(groupId)

                import time
                time.sleep(120)
                service.closeStream()
            else:
                service.goOffline()
                service.closeStream()
                exit()
        except Exception as e:
            service.goOffline()
            exit()


main()
