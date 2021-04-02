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
    return hashlib.sha256(password.encode()).hexdigest()


def successMessage(msg):
    print(bcolors.OKGREEN, "[i]",  msg)


def warningMessage(msg):
    print(bcolors.WARNING, "[!]", msg)


def errorMessage(msg):
    print(bcolors.FAIL, "[x]", msg)


def customMessage(msg):
    row = len(msg)
    h = ''.join(['+'] + ['-' * row] + ['+'])
    result = h + '\n'"|"+msg+"|"'\n' + h
    print(result)


def leftPrint(msg):
    print("{0:^15} ".format(msg))


def rightPrint(msg):
    print("{0:>100} ".format(msg))


def displayFeatures():
    x = PrettyTable()
    x.field_names = ["FireChat Features"]
    x.align = "l"
    x.padding_width = 5
    x.add_row(["[✔] Authentication"])
    x.add_row(["[✔] Get user profile"])
    x.add_row(["[✔] Send\View messages"])
    x.add_row(["[✔] Realtime messaging using streams"])
    x.add_row(["[✔] Mapping b\w username and id"])
    x.add_row(["[✔] See online users"])
    print(x)
