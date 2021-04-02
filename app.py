from utils.utils import successMessage, leftPrint, rightPrint, customMessage, warningMessage, displayFeatures
from services.firebaseservice import FirebaseService


def main():
    successMessage("Starting FireChat")
    service = FirebaseService("usttest-89c43-default-rtdb")

    displayFeatures()

    exit()

    while True:

        if service.currentUser != None:
            customMessage("     Logged in as  " +
                          service.currentUser.getName()+"       "+"ID :> "+str(service.currentUser.getId()))
        else:
            customMessage("     You are not logged in.      ")
        try:
            choice = int(
                input("1: Signup\n2: Signin\n3: Get Current User\n4: Send message\n5: See messages from user\n6: Lookup directory\n7: See online users\n8: Stream chat\n\n:>"))

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

            else:
                service.goOffline()
                service.closeStream()
                exit()
        except Exception as e:
            print(e)
            service.goOffline()
            exit()


main()
