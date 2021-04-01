from utils.utils import successMessage, leftPrint, rightPrint, customMessage
from services.firebaseservice import FirebaseService


def main():
    successMessage("Starting application")
    service = FirebaseService("usttest-89c43-default-rtdb")

    while True:

        if service.currentUser != None:
            customMessage("     Logged in as  " +
                          service.currentUser.getName()+"       "+"ID :> "+str(service.currentUser.getId()))
        else:
            customMessage("     You are not logged in.      ")
        try:
            choice = int(
                input("1: Signup\n2: Signin\n3: Get Current User\n4: Send message\n5: See messages from user\n6: Lookup directory\n7: See online users\n\n:>"))

            if choice == 1:
                username = input("Username :> ")
                id = int(input("ID :> "))
                password = input("Password :> ")
                service.signUpUser(username, id, password)
            elif choice == 2:
                username = input("Username :> ")
                password = input("Password :> ")
                service.signInUser(username,  password)
                service.updatesMessagesForUsers()

            elif choice == 3:
                print("")
                print(service.getCurrentUser())
                print("")
            elif choice == 4:
                receiverId = int(input("Receiver id :> "))
                while True:
                    msg = input(":> ")
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
            else:
                service.goOffline()
                exit()
        except:
            service.goOffline()
            exit()


main()
