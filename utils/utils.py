import hashlib


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
    print()
    print(result)
    print()


def leftPrint(msg):
    print("{0:^15} ".format(msg))


def rightPrint(msg):
    print("{0:>100} ".format(msg))
