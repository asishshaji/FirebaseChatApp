import hashlib
from prettytable import PrettyTable


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def hashPassword(password):
    """Hash of the password

    Args:
        password (str): password

    Returns:
        str: hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def successMessage(msg):
    print(bcolors.OKGREEN + "[i]", msg)


def warningMessage(msg):
    print(bcolors.WARNING + "[!]", msg)


def errorMessage(msg):
    print(bcolors.FAIL + "[x]", msg)


def customMessage(msg):
    row = len(msg)
    h = ''.join(['+'] + ['-' * row] + ['+'])
    result = h + '\n'"|" + msg + "|"'\n' + h
    print(result)


def leftPrint(msg):
    print("{0:^15} ".format(msg))


def rightPrint(msg):
    print("{0:>100} ".format(msg))


features = ["[✔] Authentication using sha",
            "[✔] Get user profile",
            "[✔] Send/View messages",
            "[✔] Realtime messaging using streams",
            "[✔] Mapping b/w username and id",
            "[✔] See online users",
            "[✔] Create groups",
            "[✔] Add users to groups",
            "[✔] Stream messages from groups"
            ]


def displayFeatures():
    x = PrettyTable()
    x.field_names = ["FireChat Features"]
    x.align = "l"
    x.padding_width = 5
    for feature in features:
        x.add_row([feature])

    print(x)
