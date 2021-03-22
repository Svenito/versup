from colorama import Fore, Back, Style


def print_ok(message: str):
    print(Fore.GREEN + u"\u2713 " + Fore.RESET + message + "\n")


def print_error(message: str):
    print(Fore.RED + Style.BRIGHT + u"\u2717 " + Style.RESET_ALL + message + "\n")


def print_warn(message: str):
    print(Fore.RED + Style.BRIGHT + u"! " + Style.RESET_ALL + message + "\n")
