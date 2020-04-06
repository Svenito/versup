from colorama import Fore, Back, Style


def print_ok(message):
    print(Fore.GREEN + u"\u2713 " + Fore.RESET + message + "\n")


def print_error(message):
    print(Fore.RED + Style.BRIGHT + u"\u2717 " + Style.RESET_ALL + message + "\n")
